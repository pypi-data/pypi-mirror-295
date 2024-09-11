# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import configparser
import contextlib
import datetime
import json
import logging
import os
import re
from collections.abc import AsyncIterator, Iterator
from functools import partial
from pathlib import Path
from typing import Any

from dateutil.tz import gettz
from pgtoolkit import conf as pgconf

from .. import cmd, conf, exceptions, postgresql, types, util
from ..models import interface, system
from ..postgresql.ctl import libpq_environ
from ..settings import Settings, _pgbackrest
from ..task import task
from .models import interface as i
from .models import system as s

logger = logging.getLogger(__name__)


def available(settings: Settings) -> _pgbackrest.Settings | None:
    return settings.pgbackrest


def get_settings(settings: Settings) -> _pgbackrest.Settings:
    """Return settings for pgbackrest

    Same as `available` but assert that settings are not None.
    Should be used in a context where settings for the plugin are surely
    set (for example in hookimpl).
    """
    assert settings.pgbackrest is not None
    return settings.pgbackrest


def rolename(settings: Settings) -> str:
    return settings.postgresql.backuprole.name


def role(settings: Settings, manifest: interface.Instance) -> interface.Role | None:
    name = rolename(settings)
    service_manifest = manifest.service(i.Service)
    extra = {}
    if settings.postgresql.auth.passfile is not None:
        extra["pgpass"] = settings.postgresql.backuprole.pgpass
    return interface.Role(
        name=name,
        password=service_manifest.password,
        login=True,
        superuser=True,
        **extra,
    )


def enabled(
    instance: system.PostgreSQLInstance, settings: _pgbackrest.Settings
) -> bool:
    return system_lookup(instance.datadir, settings) is not None


def base_configpath(settings: _pgbackrest.Settings) -> Path:
    return settings.configpath / "pgbackrest.conf"


def config_directory(settings: _pgbackrest.Settings) -> Path:
    return settings.configpath / "conf.d"


def create_include_directory(settings: _pgbackrest.Settings) -> None:
    if not (d := config_directory(settings)).exists():
        logger.info("creating pgBackRest include directory")
        d.mkdir(mode=0o750, exist_ok=True, parents=True)


def delete_include_directory(settings: _pgbackrest.Settings) -> None:
    if (d := config_directory(settings)).exists():
        logger.info("deleting pgBackRest include directory")
        util.rmdir(d)


def make_cmd(stanza: str, settings: _pgbackrest.Settings, *args: str) -> list[str]:
    return [
        str(settings.execpath),
        f"--config-path={settings.configpath}",
        "--log-level-stderr=info",
        f"--stanza={stanza}",
    ] + list(args)


parser = partial(configparser.ConfigParser, strict=True)

pgpath_rgx = re.compile(r"pg(\d+)-path")


def next_index(cp: configparser.ConfigParser, stanza: str) -> int:
    """Return the next index of pgN- options in parser.

    >>> cp = parser()
    >>> next_index(cp, "st")
    Traceback (most recent call last):
        ...
    configparser.NoSectionError: No section: 'st'
    >>> cp.add_section("st")
    >>> next_index(cp, "st")
    1
    >>> cp["st"]["pg1-path"] = "/pgsql/main"
    >>> next_index(cp, "st")
    2
    """
    idxs = {0}
    for opt in cp.options(stanza):
        if m := pgpath_rgx.match(opt):
            idxs.add(int(m.group(1)))
    return max(idxs) + 1


def system_lookup(datadir: Path, settings: _pgbackrest.Settings) -> s.Service | None:
    d = config_directory(settings)
    for p in d.glob("*.conf"):
        cp = parser()
        with p.open() as f:
            cp.read_file(f)
        for stanza in cp.sections():
            for key, value in cp.items(stanza):
                if (m := pgpath_rgx.match(key)) and value == str(datadir):
                    return s.Service(stanza=stanza, path=p, index=int(m.group(1)))
    logger.debug(
        "no pgBackRest configuration file matching PGDATA=%s found in %s", datadir, d
    )
    return None


def stanza_pgpaths(path: Path, stanza: str) -> Iterator[tuple[int, Path]]:
    cp = parser()
    with path.open() as f:
        cp.read_file(f)
    for key, value in cp.items(stanza):
        if m := pgpath_rgx.match(key):
            yield int(m.group(1)), Path(value)


def service(
    instance: system.PostgreSQLInstance,
    manifest: i.Service,
    settings: _pgbackrest.Settings,
    upgrading_from: interface.InstanceRef | None,
) -> s.Service:
    """Retrieve a Service object.

    In case of an upgrade, if a service exists on original 'upgrading_from'
    instance, return it.

    Otherwise, lookup for a service bound to 'instance' and return it if
    found.

    Fall back to building a new service object from scratch.
    """
    if upgrading_from:
        if svc := system_lookup(upgrading_from.datadir, settings):
            return svc
    if svc := system_lookup(instance.datadir, settings):
        if manifest.stanza != svc.stanza:
            raise exceptions.InstanceStateError(
                f"instance {instance} is already bound to pgbackrest stanza {svc.stanza!r} (path={svc.path})"
            )
        return svc
    stanza = manifest.stanza
    index = 1
    path = config_directory(settings) / f"{stanza}.conf"
    # Use the next pgN index when the path exists but configured instance is
    # not attached to its stanza. This would typically happen for standby
    # instances, when created on the same host as the primary.
    if path.exists():
        cp = parser()
        with path.open() as f:
            cp.read_file(f)
        index = next_index(cp, stanza)
    return s.Service(stanza=stanza, path=path, index=index)


async def backup_info(
    service: s.Service,
    settings: _pgbackrest.Settings,
    *,
    backup_set: str | None = None,
) -> dict[str, Any]:
    """Call pgbackrest info command to obtain information about backups.

    Ref.: https://pgbackrest.org/command.html#command-info
    """
    args = []
    if backup_set is not None:
        args.append(f"--set={backup_set}")
    args.extend(["--output=json", "info"])
    r = await cmd.asyncio_run(make_cmd(service.stanza, settings, *args), check=True)
    infos = json.loads(r.stdout)
    try:
        return next(i for i in infos if i["name"] == service.stanza)
    except StopIteration:
        return {}


@task
def setup(
    service: s.Service,
    settings: _pgbackrest.Settings,
    instance_config: pgconf.Configuration,
    changes: types.ConfigChanges,
    creating: bool,
    datadir: Path,
    backuprole: str,
) -> None:
    """Setup pgBackRest"""
    if not creating and not any(
        s in changes for s in ("port", "unix_socket_directories")
    ):
        return

    base_config_path = base_configpath(settings)
    if not base_config_path.exists():
        raise exceptions.SystemError(
            f"Missing base config file {base_config_path} for pgbackrest. "
            "Did you forget to run 'pglift site-configure'?"
        )

    stanza = service.stanza
    stanza_confpath = service.path
    pg = f"pg{service.index}"
    cp = parser()
    if stanza_confpath.exists():
        with stanza_confpath.open() as f:
            cp.read_file(f)

    logger.info(
        "configuring pgBackRest stanza '%s' for pg%d-path=%s",
        stanza,
        service.index,
        datadir,
    )
    # Always use string values so that this would match with actual config (on
    # disk) that's parsed later on.
    config = {
        stanza: {
            f"{pg}-path": str(datadir),
            f"{pg}-port": str(conf.get_port(instance_config)),
            f"{pg}-user": backuprole,
        },
    }
    if unix_socket_directories := instance_config.get("unix_socket_directories"):
        config[stanza][f"{pg}-socket-path"] = str(unix_socket_directories)
    cp.read_dict(config)
    with stanza_confpath.open("w") as configfile:
        cp.write(configfile)


def postgresql_configuration(
    stanza: str, settings: _pgbackrest.Settings, version: str, datadir: Path
) -> pgconf.Configuration:
    pgconfig = postgresql.template(version, "pgbackrest.conf").format(
        execpath=settings.execpath,
        configpath=settings.configpath,
        stanza=stanza,
        datadir=datadir,
    )
    config = pgconf.Configuration()
    list(config.parse(pgconfig.splitlines()))
    return config


@setup.revert(title="deconfiguring pgBackRest")
def revert_setup(
    service: s.Service,
    settings: _pgbackrest.Settings,
    instance_config: pgconf.Configuration,
    changes: types.ConfigChanges,
    creating: bool,
    datadir: Path,
    backuprole: str,
) -> None:
    """Un-setup pgBackRest.

    Remove options from 'stanza' section referencing instance's datadir, then
    possibly remove the configuration file if empty, and finally remove
    stanza's log files.
    """
    stanza = service.stanza
    stanza_confpath = service.path
    if stanza_confpath.exists():
        cp = parser()
        with stanza_confpath.open() as f:
            cp.read_file(f)
        for opt in cp.options(stanza):
            if opt.startswith(f"pg{service.index}-"):
                cp.remove_option(stanza, opt)
        with stanza_confpath.open("w") as f:
            cp.write(f)
        if not cp.options(stanza):
            stanza_confpath.unlink(missing_ok=True)
    if not stanza_confpath.exists():
        for logf in settings.logpath.glob(f"{stanza}-*.log"):
            logf.unlink(missing_ok=True)


@task(title="checking pgBackRest configuration for stanza {service.stanza}")
async def check(
    instance: system.PostgreSQLInstance,
    service: s.Service,
    settings: _pgbackrest.Settings,
    password: str | None,
) -> None:
    env = os.environ.copy()
    if password is not None:
        env["PGPASSWORD"] = password
    postgresql_settings = instance._settings.postgresql
    env = libpq_environ(instance, postgresql_settings.backuprole.name, base=env)
    await cmd.asyncio_run(
        make_cmd(service.stanza, settings, "check"), check=True, env=env
    )


async def iter_backups(
    instance: system.Instance, settings: _pgbackrest.Settings
) -> AsyncIterator[i.Backup]:
    """Yield information about backups on an instance."""
    try:
        service = instance.service(s.Service)
    except ValueError:
        raise exceptions.InstanceStateError(
            f"pgBackRest service is not configured for instance {instance}"
        ) from None

    backups = (await backup_info(service, settings))["backup"]

    def started_at(entry: Any) -> float:
        return entry["timestamp"]["start"]  # type: ignore[no-any-return]

    for backup in sorted(backups, key=started_at, reverse=True):
        info_set = await backup_info(service, settings, backup_set=backup["label"])
        databases = [db["name"] for db in info_set["backup"][0]["database-ref"]]
        dtstart = datetime.datetime.fromtimestamp(backup["timestamp"]["start"])
        dtstop = datetime.datetime.fromtimestamp(backup["timestamp"]["stop"])
        yield i.Backup(
            label=backup["label"],
            size=backup["info"]["size"],
            # For a "block incremental backup", the size is not returned.
            repo_size=backup["info"]["repository"].get("size"),
            date_start=dtstart.replace(tzinfo=gettz()),
            date_stop=dtstop.replace(tzinfo=gettz()),
            type=backup["type"],
            databases=databases,
        )


def restore_command(
    service: s.Service,
    settings: _pgbackrest.Settings,
    *,
    date: datetime.datetime | None = None,
    backup_set: str | None = None,
) -> list[str]:
    """Return the pgbackrest restore command for ``service``.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    args = [
        # The delta option allows pgBackRest to handle instance data/wal
        # directories itself, without the need to clean them up beforehand.
        "--delta",
        "--link-all",
    ]
    if date is not None and backup_set is not None:
        raise exceptions.UnsupportedError(
            "date and backup_set are not expected to be both specified"
        )
    elif date is not None:
        target = date.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        args += ["--target-action=promote", "--type=time", f"--target={target}"]
    elif backup_set is not None:
        args += ["--target-action=promote", "--type=immediate", f"--set={backup_set}"]
    args.append("restore")
    return make_cmd(service.stanza, settings, *args)


async def restore(
    instance: system.Instance,
    settings: _pgbackrest.Settings,
    *,
    label: str | None = None,
    date: datetime.datetime | None = None,
) -> None:
    """Restore an instance, possibly only including specified databases.

    The instance must not be running.

    Ref.: https://pgbackrest.org/command.html#command-restore
    """
    pg_instance = instance.postgresql
    if pg_instance.standby:
        raise exceptions.InstanceReadOnlyError(pg_instance)

    try:
        service = instance.service(s.Service)
    except ValueError:
        raise exceptions.InstanceStateError(
            f"pgBackRest service is not configured for instance {instance}"
        ) from None

    logger.info("restoring instance %s with pgBackRest", instance)
    cmd_args = restore_command(service, settings, date=date, backup_set=label)
    await cmd.asyncio_run(cmd_args, check=True)


def env_for(service: s.Service, settings: _pgbackrest.Settings) -> dict[str, str]:
    return {
        "PGBACKREST_CONFIG_PATH": str(settings.configpath),
        "PGBACKREST_STANZA": service.stanza,
    }


def site_configure_install(
    settings: Settings,
    config: configparser.ConfigParser,
) -> None:
    s = get_settings(settings)
    if not (global_configpath := base_configpath(s)).exists():
        util.check_or_create_directory(
            global_configpath.parent, "base pgBackRest configuration"
        )
        logger.info("installing base pgBackRest configuration")
        with global_configpath.open("w") as f:
            config.write(f)
    create_include_directory(s)


def site_configure_uninstall(settings: Settings) -> None:
    s = get_settings(settings)
    delete_include_directory(s)
    if (global_configpath := base_configpath(s)).exists():
        logger.info("uninstalling base pgBackRest configuration")
        global_configpath.unlink(missing_ok=True)


def site_configure_check(settings: Settings, log: bool) -> Iterator[bool]:
    s = get_settings(settings)
    for p in (config_directory(s), base_configpath(s)):
        if not p.exists():
            if log:
                logger.error("pgBackRest configuration path %s missing", p)
            yield False
        else:
            yield True


@contextlib.contextmanager
def instance_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: pgconf.Configuration,
    changes: types.ConfigChanges,
    creating: bool,
) -> Iterator[system.PostgreSQLInstance]:
    yield instance
    settings = instance._settings
    s = get_settings(settings)
    service_manifest = manifest.service(i.Service)
    service_ = service(instance, service_manifest, s, manifest.upgrading_from)
    setup(
        service_,
        s,
        config,
        changes,
        creating,
        instance.datadir,
        settings.postgresql.backuprole.name,
    )


@contextlib.contextmanager
def instance_dropped(instance: system.Instance) -> Iterator[s.Service | None]:
    try:
        service = instance.service(s.Service)
    except ValueError:
        yield None
        return
    yield service
    settings = instance._settings
    pg_instance = instance.postgresql
    revert_setup(
        service,
        get_settings(settings),
        pg_instance.config(),
        {},
        False,
        pg_instance.datadir,
        settings.postgresql.backuprole.name,
    )
