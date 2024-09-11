# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
import logging
import os
import re
import shutil
import tempfile
import time
from collections.abc import AsyncIterator, Iterator
from functools import partial
from pathlib import Path

import psycopg.rows
import psycopg.sql
from pgtoolkit import conf as pgconf
from pgtoolkit import pgpass
from tenacity import AsyncRetrying
from tenacity.before_sleep import before_sleep_log
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_delay
from tenacity.wait import wait_exponential

from . import (
    async_hook,
    async_hooks,
    cmd,
    conf,
    databases,
    db,
    exceptions,
    h,
    hook,
    hooks,
    plugin_manager,
    postgresql,
    roles,
    ui,
    util,
)
from .models import interface, system
from .postgresql.ctl import get_data_checksums, libpq_environ, set_data_checksums
from .postgresql.ctl import log as postgresql_log
from .settings import Settings, default_postgresql_version
from .settings._postgresql import PostgreSQLVersion
from .task import task
from .types import ConfigChanges, PostgreSQLStopMode, Status, validation_context

logger = logging.getLogger(__name__)


@task(title="initializing PostgreSQL")
async def init(
    instance: system.PostgreSQLInstance, manifest: interface.Instance
) -> bool:
    """Initialize a PostgreSQL cluster."""
    settings = instance._settings
    settings.postgresql.socket_directory.mkdir(parents=True, exist_ok=True)

    await async_hook(settings, h.initdb, manifest=manifest, instance=instance)

    is_running = await postgresql.is_running(instance)

    if (
        hook(settings, h.configure_auth, instance=instance, manifest=manifest)
        and is_running
    ):
        await async_hook(
            settings, h.restart_postgresql, instance=instance, mode="fast", wait=True
        )

    psqlrc = postgresql.template(manifest.version, "psqlrc")
    instance.psqlrc.write_text(psqlrc.format(instance=instance))

    service = hook(settings, h.postgresql_service_name, instance=instance)
    assert service is not None
    await async_hook(
        settings,
        h.enable_service,
        settings=settings,
        service=service,
        name=instance.qualname,
    )

    return is_running


@init.revert(title="deleting PostgreSQL cluster")
async def revert_init(
    instance: system.PostgreSQLInstance, manifest: interface.Instance
) -> None:
    """Un-initialize a PostgreSQL cluster."""
    settings = instance._settings
    service = hook(settings, h.postgresql_service_name, instance=instance)
    assert service is not None
    await async_hook(
        settings,
        h.disable_service,
        settings=settings,
        service=service,
        name=instance.qualname,
        now=True,
    )

    for path in (instance.datadir, instance.waldir):
        if path.exists():
            util.rmtree(path)


async def configure(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    *,
    run_hooks: bool = True,
    _creating: bool = False,
    _is_running: bool | None = None,
) -> ConfigChanges:
    """Write instance's configuration in postgresql.conf."""
    async with configure_context(
        instance,
        manifest,
        run_hooks=run_hooks,
        creating=_creating,
        is_running=_is_running,
    ) as changes:
        return changes


@contextlib.asynccontextmanager
async def configure_context(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    *,
    run_hooks: bool = True,
    creating: bool = False,
    is_running: bool | None = None,
) -> AsyncIterator[ConfigChanges]:
    """Context manager to write instance's configuration in postgresql.conf
    while pausing for further actions before calling 'instance_configured'
    hooks.

    Also compute changes to the overall PostgreSQL configuration and return it
    as a 'ConfigChanges' dictionary.

    When resuming to call instance_configured hooks, PostgreSQL messages are
    forwarded to our logger if the current log file exists.
    """
    logger.info("configuring PostgreSQL")
    s = instance._settings
    config = configuration(manifest, s)
    changes = await async_hook(
        s,
        h.configure_postgresql,
        manifest=manifest,
        configuration=config,
        instance=instance,
    )
    assert changes is not None

    yield changes

    if run_hooks:
        async with postgresql_log(instance):
            await async_hooks(
                s,
                h.instance_configured,
                instance=instance,
                manifest=manifest,
                config=config,
                changes=changes,
                creating=creating,
            )

    if is_running is None:
        is_running = (await postgresql.status(instance)) == Status.running
    if not creating and is_running:
        await check_pending_actions(instance, changes, manifest.restart_on_changes)


def configuration(
    manifest: interface.Instance,
    settings: Settings,
    *,
    template: str | None = None,
) -> pgconf.Configuration:
    """Return the PostgreSQL configuration built from manifest and
    'postgresql.conf' site template (the former taking precedence over the
    latter).

    'shared_buffers' and 'effective_cache_size' setting, if defined and set to
    a percent-value, will be converted to proper memory value relative to the
    total memory available on the system.
    """
    if template is None:
        template = postgresql.template(manifest.version, "postgresql.conf")
    # Load base configuration from site settings.
    try:
        confitems = pgconf.parse_string(template).as_dict()
    except pgconf.ParseError as e:
        raise exceptions.SettingsError(f"invalid postgresql.conf template: {e}") from e

    # Transform initdb options as configuration parameters.
    if locale := manifest.initdb_options(settings.postgresql.initdb).locale:
        for key in ("lc_messages", "lc_monetary", "lc_numeric", "lc_time"):
            confitems.setdefault(key, locale)

    if manifest.port is not None:
        confitems["port"] = manifest.port
    confitems.update(manifest.settings)

    spl = confitems.get("shared_preload_libraries", "")
    if not isinstance(spl, str):
        raise exceptions.InstanceStateError(
            f"expecting a string value for 'shared_preload_libraries' setting: {spl!r}"
        )

    for r in hooks(settings, h.instance_settings, manifest=manifest, settings=settings):
        for k, v in r.entries.items():
            if k == "shared_preload_libraries":
                assert isinstance(v.value, str), f"expecting a string, got {v.value!r}"
                spl = conf.merge_lists(spl, v.value)
            else:
                confitems[k] = v.value

    if spl:
        confitems["shared_preload_libraries"] = spl

    conf.format_values(confitems, manifest.name, manifest.version, settings.postgresql)

    return conf.make(**confitems)


@contextlib.asynccontextmanager
async def stopped(
    instance: system.Instance, *, timeout: int = 10
) -> AsyncIterator[None]:
    """Context manager to temporarily stop an instance.

    :param timeout: delay to wait for instance stop.

    :raises ~exceptions.InstanceStateError: when the instance did stop after
        specified `timeout` (in seconds).
    """
    pg_instance = instance.postgresql
    if (await postgresql.status(pg_instance)) == Status.not_running:
        yield
        return

    await stop(instance)
    for __ in range(timeout):
        time.sleep(1)
        if (await postgresql.status(pg_instance)) == Status.not_running:
            break
    else:
        raise exceptions.InstanceStateError(f"{instance} not stopped after {timeout}s")
    try:
        yield
    finally:
        await start(instance)


async def start(
    instance: system.Instance,
    *,
    foreground: bool = False,
    wait: bool = True,
    _check: bool = True,
) -> None:
    """Start an instance.

    :param wait: possibly wait for PostgreSQL to get ready.
    :param foreground: start postgres in the foreground, replacing the current
        process.

    .. note:: When starting in "foreground", hooks will not be triggered and
        `wait` parameter have no effect.
    """
    await _start_postgresql(
        instance.postgresql, foreground=foreground, wait=wait, check=_check
    )
    if wait:
        if foreground:
            logger.debug("not running hooks for a foreground start")
        else:
            await async_hooks(instance._settings, h.instance_started, instance=instance)


async def _start_postgresql(
    instance: system.PostgreSQLInstance,
    *,
    foreground: bool = False,
    wait: bool = True,
    check: bool = True,
) -> None:
    if check and await postgresql.is_running(instance):
        logger.warning("instance %s is already started", instance)
        return
    settings = instance._settings
    settings.postgresql.socket_directory.mkdir(parents=True, exist_ok=True)
    await async_hook(
        settings,
        h.start_postgresql,
        instance=instance,
        foreground=foreground,
        wait=wait,
    )


async def stop(
    instance: system.Instance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
    deleting: bool = False,
) -> None:
    """Stop an instance."""
    s = instance._settings
    pg_instance = instance.postgresql
    if await postgresql.status(pg_instance) == Status.not_running:
        logger.warning("instance %s is already stopped", instance)
    else:
        await async_hook(
            s,
            h.stop_postgresql,
            instance=pg_instance,
            mode=mode,
            wait=wait,
            deleting=deleting,
        )

    if wait:
        await async_hooks(s, h.instance_stopped, instance=instance)


async def restart(
    instance: system.Instance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
) -> None:
    """Restart an instance."""
    logger.info("restarting instance %s", instance)
    s = instance._settings
    await async_hooks(s, h.instance_stopped, instance=instance)
    await restart_postgresql(instance.postgresql, mode=mode, wait=wait)
    await async_hooks(s, h.instance_started, instance=instance)


async def restart_postgresql(
    instance: system.PostgreSQLInstance,
    *,
    mode: PostgreSQLStopMode = "fast",
    wait: bool = True,
) -> None:
    s = instance._settings
    service = hook(s, h.postgresql_service_name, instance=instance)
    assert service is not None
    if await async_hook(
        s,
        h.restart_service,
        settings=s,
        service=service,
        name=instance.qualname,
    ):
        await postgresql.wait_ready(instance)
    else:
        await async_hook(
            s, h.restart_postgresql, instance=instance, mode=mode, wait=wait
        )


async def reload(instance: system.PostgreSQLInstance) -> None:
    """Reload an instance."""
    async with postgresql_log(instance):
        await async_hook(instance._settings, h.reload_postgresql, instance=instance)


async def promote(instance: system.Instance) -> None:
    """Promote a standby instance"""
    pg_instance = instance.postgresql
    if not pg_instance.standby:
        raise exceptions.InstanceStateError(f"{instance} is not a standby")
    s = instance._settings
    async with postgresql_log(pg_instance):
        await async_hook(s, h.promote_postgresql, instance=pg_instance)
        await async_hooks(s, h.instance_promoted, instance=instance)


async def upgrade(
    instance: system.Instance,
    *,
    version: str | None = None,
    name: str | None = None,
    port: int | None = None,
    jobs: int | None = None,
    extra_opts: tuple[str, ...] = (),
    _instance_model: type[interface.Instance] | None = None,
) -> system.Instance:
    """Upgrade a primary instance using pg_upgrade"""
    settings = instance._settings
    pg_instance = instance.postgresql
    hooks(settings, h.check_instance_is_upgradable, instance=pg_instance)
    postgresql_settings = settings.postgresql
    if version is None:
        version = default_postgresql_version(postgresql_settings)
    if pg_instance.standby:
        raise exceptions.InstanceReadOnlyError(pg_instance)
    if pg_instance.version > version:
        raise exceptions.InvalidVersion(
            f"Could not upgrade {instance} from {pg_instance.version} to {version}"
        )
    if (name is None or name == pg_instance.name) and version == pg_instance.version:
        raise exceptions.InvalidVersion(
            f"Could not upgrade {instance} using same name and same version"
        )
    # check if target name/version already exists
    if exists((pg_instance.name if name is None else name), version, settings):
        raise exceptions.InstanceAlreadyExists(
            f"Could not upgrade {instance}: target name/version instance already exists"
        )

    surole_name = postgresql_settings.surole.name
    surole_password = libpq_environ(instance.postgresql, surole_name).get("PGPASSWORD")
    if (
        not surole_password
        and postgresql_settings.auth.passfile
        and postgresql_settings.auth.passfile.exists()
    ):
        passfile = pgpass.parse(postgresql_settings.auth.passfile)
        for entry in passfile:
            if entry.matches(port=pg_instance.port, username=surole_name):
                surole_password = entry.password
    surole = interface.Role(name=surole_name, password=surole_password)

    if _instance_model is None:
        pm = plugin_manager(settings)
        _instance_model = interface.Instance.composite(pm)

    old_manifest = await _get(instance, Status.not_running)
    data = dict(
        old_manifest,
        name=name or pg_instance.name,
        version=version,
        port=port or pg_instance.port,
        state="stopped",
        surole_password=surole.password,
        upgrading_from={
            "name": pg_instance.name,
            "version": pg_instance.version,
            "port": pg_instance.port,
            "datadir": pg_instance.datadir,
        },
    )
    with validation_context(operation="create", settings=settings):
        new_manifest = _instance_model.model_validate(data)

    if not ui.confirm(
        f"Confirm upgrade of instance {instance} to version {version}?", True
    ):
        raise exceptions.Cancelled(f"upgrade of instance {instance} cancelled")

    with system.PostgreSQLInstance.creating(
        new_manifest.name, new_manifest.version, settings
    ) as new_pg_instance:
        await _upgrade(
            pg_instance,
            new_pg_instance,
            new_manifest,
            surole,
            jobs=jobs,
            extra_opts=extra_opts,
        )
    return system.Instance.from_postgresql(new_pg_instance)


@task(title="upgrading instance {instance} as {newinstance}")
async def _upgrade(
    instance: system.PostgreSQLInstance,
    newinstance: system.PostgreSQLInstance,
    new_manifest: interface.Instance,
    surole: interface.Role,
    *,
    jobs: int | None = None,
    extra_opts: tuple[str, ...] = (),
) -> None:
    is_running = await init(newinstance, new_manifest)

    await configure(
        newinstance,
        new_manifest,
        _creating=True,
        run_hooks=False,
        _is_running=is_running,
    )
    pg_upgrade = str(newinstance.bindir / "pg_upgrade")
    cmd_args = [
        pg_upgrade,
        f"--old-bindir={instance.bindir}",
        f"--new-bindir={newinstance.bindir}",
        f"--old-datadir={instance.datadir}",
        f"--new-datadir={newinstance.datadir}",
        f"--username={surole.name}",
    ]
    if jobs is not None:
        cmd_args.extend(["--jobs", str(jobs)])
    cmd_args.extend(extra_opts)
    env = libpq_environ(instance, surole.name)
    if surole.password:
        env.setdefault("PGPASSWORD", surole.password.get_secret_value())
    logger.info("upgrading instance with pg_upgrade")
    with tempfile.TemporaryDirectory() as tmpdir:
        await cmd.asyncio_run(cmd_args, check=True, cwd=tmpdir, env=env)
    settings = newinstance._settings
    hooks(settings, h.instance_upgraded, old=instance, new=newinstance)
    await apply(settings, new_manifest, _creating=True)


@_upgrade.revert(title="dropping upgraded instance {newinstance}")
async def revert__upgrade(
    instance: system.PostgreSQLInstance,
    newinstance: system.PostgreSQLInstance,
    new_manifest: interface.Instance,
    surole: interface.Role,
    *,
    jobs: int | None = None,
    extra_opts: tuple[str, ...] = (),
) -> None:
    if newinstance.datadir.exists():
        to_drop = system.Instance.from_postgresql(newinstance)
        await drop(to_drop)


async def get_locale(cnx: db.Connection) -> str | None:
    """Return the value of instance locale.

    If locale subcategories are set to distinct values, return None.
    """
    locales = {
        s.name: s.setting for s in await settings(cnx) if s.name.startswith("lc_")
    }
    values = set(locales.values())
    if len(values) == 1:
        return values.pop()
    else:
        logger.debug(
            "cannot determine instance locale, settings are heterogeneous: %s",
            ", ".join(f"{n}: {s}" for n, s in sorted(locales.items())),
        )
        return None


async def apply(
    settings: Settings,
    instance: interface.Instance,
    *,
    _creating: bool = False,
    _is_running: bool | None = None,
) -> interface.InstanceApplyResult:
    """Apply state described by interface model as a PostgreSQL instance.

    Depending on the previous state and existence of the target instance, the
    instance may be created or updated or dropped.

    If configuration changes are detected and the instance was previously
    running, the server will be reloaded automatically; if a restart is
    needed, the user will be prompted in case of interactive usage or this
    will be performed automatically if 'restart_on_changes' is set to True.
    """
    if (state := instance.state) == "absent":
        dropped = False
        if exists(instance.name, instance.version, settings):
            await drop(
                system.Instance.system_lookup(instance.name, instance.version, settings)
            )
            dropped = True
        return interface.InstanceApplyResult(
            change_state="dropped" if dropped else None
        )

    changed = False
    try:
        pg_instance = system.PostgreSQLInstance.system_lookup(
            instance.name, instance.version, settings
        )
    except exceptions.InstanceNotFound:
        pg_instance = None
    if pg_instance is None:
        _creating = True
        with system.PostgreSQLInstance.creating(
            instance.name, instance.version, settings
        ) as pg_instance:
            _is_running = await init(pg_instance, instance)
        changed = True

    if _is_running is None:
        _is_running = await postgresql.is_running(pg_instance)

    surole = instance.surole(settings)
    superuser_connect = partial(
        db.connect,
        pg_instance,
        user=surole.name,
        password=(
            surole.password.get_secret_value() if surole.password is not None else None
        ),
    )

    async with configure_context(
        pg_instance,
        instance,
        is_running=_is_running,
        creating=_creating,
    ) as changes:
        if state in ("started", "restarted") and not _is_running:
            await _start_postgresql(pg_instance, check=False)
            _is_running = True
        if _creating:
            # Now that PostgreSQL configuration is done, call hooks for
            # super-user role creation (handled by initdb), e.g. to create the
            # .pgpass entry.
            instance_roles = hooks(
                settings, h.role, settings=settings, manifest=instance
            )
            hooks(settings, h.role_change, role=surole, instance=pg_instance)
            if pg_instance.standby or instance.upgrading_from:
                # Just apply role changes here (e.g. .pgpass entries).
                # This concerns standby instances, which are read-only, as
                # well as upgraded instances, in which objects (roles and
                # databases) would be migrated as is.
                for role in instance_roles:
                    hooks(settings, h.role_change, role=role, instance=pg_instance)
            else:

                async def apply_databases_and_roles() -> bool:
                    changed = False
                    async with superuser_connect() as cnx:
                        await wait_recovery_finished(cnx)
                        replrole = instance.replrole(settings)
                        if replrole:
                            if (
                                await roles._apply(cnx, replrole, pg_instance)
                            ).change_state:
                                changed = True
                        for role in instance_roles:
                            if (
                                await roles._apply(cnx, role, pg_instance)
                            ).change_state:
                                changed = True
                        for database in hooks(
                            settings, h.database, settings=settings, manifest=instance
                        ):
                            if (
                                await databases._apply(cnx, database, pg_instance)
                            ).change_state:
                                changed = True
                    return changed

                if _is_running:
                    changed = await apply_databases_and_roles()
                else:
                    async with postgresql.running(pg_instance):
                        changed = await apply_databases_and_roles()

    changed = changed or bool(changes)

    if instance.data_checksums is not None:
        actual_data_checksums = await get_data_checksums(pg_instance)
        if actual_data_checksums != instance.data_checksums:
            if instance.data_checksums:
                logger.info("enabling data checksums")
            else:
                logger.info("disabling data checksums")
            if _is_running:
                raise exceptions.InstanceStateError(
                    "cannot alter data_checksums on a running instance"
                )
            await set_data_checksums(pg_instance, instance.data_checksums)
            changed = True

    sys_instance = system.Instance.from_postgresql(pg_instance)

    if state == "stopped":
        if _is_running:
            await stop(sys_instance)
            changed = True
            _is_running = False
    elif state in ("started", "restarted"):
        if state == "started":
            if not _is_running:
                await start(sys_instance, _check=False)
            else:
                await async_hooks(settings, h.instance_started, instance=sys_instance)
        elif state == "restarted":
            await restart(sys_instance)
        changed = True
        _is_running = True
    else:
        # TODO: use typing.assert_never() instead
        # https://typing.readthedocs.io/en/latest/source/unreachable.html
        assert False, f"unexpected state: {state}"  # noqa: B011  # pragma: nocover

    standby = instance.standby

    if standby and standby.status == "promoted" and pg_instance.standby is not None:
        await promote(sys_instance)

    if not pg_instance.standby and (instance.roles or instance.databases):
        async with postgresql.running(pg_instance):
            for a_role in instance.roles:
                r = await roles.apply(pg_instance, a_role)
                changed = r.change_state in ("created", "changed") or changed
            for a_database in instance.databases:
                r = await databases.apply(pg_instance, a_database)
                changed = r.change_state in ("changed", "created") or changed
    change_state, p_restart = None, False
    if _creating:
        change_state = "created"
    elif changed:
        change_state = "changed"
        if _is_running:
            async with superuser_connect() as cnx:
                p_restart = await pending_restart(cnx)
    return interface.InstanceApplyResult(
        change_state=change_state, pending_restart=p_restart
    )


async def pending_restart(cnx: db.Connection) -> bool:
    """Return True if the instance is pending a restart to account for configuration changes."""
    async with cnx.cursor(row_factory=psycopg.rows.args_row(bool)) as cur:
        await cur.execute("SELECT bool_or(pending_restart) FROM pg_settings")
        row = await cur.fetchone()
        assert row is not None
        return row


async def check_pending_actions(
    instance: system.PostgreSQLInstance,
    changes: ConfigChanges,
    restart_on_changes: bool,
) -> None:
    """Check if any of the changes require a reload or a restart.

    The instance is automatically reloaded if needed.
    The user is prompted for confirmation if a restart is needed.

    The instance MUST be running.
    """
    if "port" in changes:
        needs_restart = True
    else:
        needs_restart = False
        pending_restart = set()
        pending_reload = set()
        async with db.connect(instance) as cnx:
            for p in await settings(cnx):
                pname = p.name
                if pname not in changes:
                    continue
                if p.context == "postmaster":
                    pending_restart.add(pname)
                else:
                    pending_reload.add(pname)

        if pending_reload:
            logger.info(
                "instance %s needs reload due to parameter changes: %s",
                instance,
                ", ".join(sorted(pending_reload)),
            )
            await reload(instance)

        if pending_restart:
            logger.warning(
                "instance %s needs restart due to parameter changes: %s",
                instance,
                ", ".join(sorted(pending_restart)),
            )
            needs_restart = True

    if needs_restart and ui.confirm(
        "PostgreSQL needs to be restarted; restart now?", restart_on_changes
    ):
        await restart_postgresql(instance)


async def get(instance: system.Instance) -> interface.Instance:
    """Return a interface Instance model from a system Instance."""
    pg_instance = instance.postgresql
    status = await postgresql.status(pg_instance)
    if status != Status.running:
        missing_bits = [
            "locale",
            "encoding",
            "passwords",
            "pending_restart",
        ]
        if pg_instance.standby is not None:
            missing_bits.append("replication lag")
        logger.warning(
            "instance %s is not running, information about %s may not be accurate",
            instance,
            f"{', '.join(missing_bits[:-1])} and {missing_bits[-1]}",
        )
    return await _get(instance, status)


async def _get(instance: system.Instance, status: Status) -> interface.Instance:
    settings = instance._settings
    pg_instance = instance.postgresql
    config = pg_instance.config()
    managed_config = config.as_dict()
    managed_config.pop("port", None)
    state = interface.state_from_pg_status(status)
    instance_is_running = status == Status.running
    services = {
        s.__class__.__service__: s
        for s in await async_hooks(
            settings, h.get, instance=instance, running=instance_is_running
        )
        if s is not None
    }

    standby = None
    if pg_instance.standby:
        try:
            standby = await async_hook(
                settings,
                h.standby_model,
                instance=pg_instance,
                standby=pg_instance.standby,
                running=instance_is_running,
            )
        except ValueError:
            pass

    locale = None
    encoding = None
    data_checksums = None
    pending_rst = False
    if instance_is_running:
        async with db.connect(pg_instance, dbname="template1") as cnx:
            locale = await get_locale(cnx)
            encoding = await databases.encoding(cnx)
            pending_rst = await pending_restart(cnx)
    data_checksums = await get_data_checksums(pg_instance)

    return interface.Instance(
        name=instance.name,
        version=pg_instance.version,
        port=pg_instance.port,
        state=state,
        pending_restart=pending_rst,
        settings=managed_config,
        locale=locale,
        encoding=encoding,
        data_checksums=data_checksums,
        standby=standby,
        **{"data_directory": pg_instance.datadir, "wal_directory": pg_instance.waldir},
        **services,
    )


async def drop(instance: system.Instance) -> None:
    """Drop an instance."""
    logger.info("dropping instance %s", instance)
    if not ui.confirm(f"Confirm complete deletion of instance {instance}?", True):
        raise exceptions.Cancelled(f"deletion of instance {instance} cancelled")

    await stop(instance, mode="immediate", deleting=True)

    settings = instance._settings
    pg_instance = instance.postgresql
    await async_hooks(settings, h.instance_dropped, instance=instance)
    for rolename in hooks(settings, h.rolename, settings=settings):
        hooks(
            settings,
            h.role_change,
            role=interface.Role(name=rolename, state="absent"),
            instance=pg_instance,
        )
    manifest = interface.Instance(name=instance.name, version=pg_instance.version)
    await revert_init(instance.postgresql, manifest)


async def ls(
    settings: Settings, *, version: PostgreSQLVersion | None = None
) -> AsyncIterator[interface.InstanceListItem]:
    """Yield instances found by system lookup.

    :param version: filter instances matching a given version.

    :raises ~exceptions.InvalidVersion: if specified version is unknown.
    """
    for instance in system_list(settings, version=version):
        status = await postgresql.status(instance)
        yield interface.InstanceListItem(
            name=instance.name,
            datadir=instance.datadir,
            port=instance.port,
            status=status.name,
            version=instance.version,
        )


def system_list(
    settings: Settings, *, version: PostgreSQLVersion | None = None
) -> Iterator[system.PostgreSQLInstance]:
    if version is not None:
        assert isinstance(version, PostgreSQLVersion)
        versions = [version.value]
    else:
        versions = [v.version for v in settings.postgresql.versions]

    # Search for directories matching datadir template globing on the part
    # containing {name}. Since the {version} part may come after or before
    # {name}, we first build a datadir for each known version and split it
    # on part containing {name} for further globbing.
    name_idx = next(
        i
        for i, item in enumerate(settings.postgresql.datadir.parts)
        if "{name}" in item
    )

    for ver in versions:
        version_path = Path(
            str(settings.postgresql.datadir).format(name="*", version=ver)
        )
        prefix = Path(*version_path.parts[:name_idx])
        suffix = Path(*version_path.parts[name_idx + 1 :])
        pattern = re.compile(
            str(settings.postgresql.datadir).format(name="(.*)", version=ver)
        )
        for d in sorted(prefix.glob(f"*/{suffix}")):
            if not d.is_dir():
                continue
            matches = re.match(pattern, str(d))
            if not matches:
                continue
            name = matches.groups()[0]
            try:
                yield system.PostgreSQLInstance.system_lookup(name, ver, settings)
            except exceptions.InstanceNotFound:
                pass


def env_for(instance: system.Instance, *, path: bool = False) -> dict[str, str]:
    """Return libpq environment variables suitable to connect to `instance`.

    If 'path' is True, also inject PostgreSQL binaries directory in PATH.
    """
    settings = instance._settings
    postgresql_settings = settings.postgresql
    pg_instance = instance.postgresql
    env = libpq_environ(pg_instance, postgresql_settings.surole.name, base={})
    env.update(
        {
            "PGUSER": postgresql_settings.surole.name,
            "PGPORT": str(pg_instance.port),
            "PGDATA": str(pg_instance.datadir),
            "PSQLRC": str(pg_instance.psqlrc),
            "PSQL_HISTORY": str(pg_instance.psql_history),
        }
    )
    if sd := pg_instance.socket_directory:
        env["PGHOST"] = sd
    if path:
        env["PATH"] = ":".join(
            [str(pg_instance.bindir)]
            + ([os.environ["PATH"]] if "PATH" in os.environ else [])
        )
    for env_vars in hooks(settings, h.instance_env, instance=instance):
        env.update(env_vars)
    return env


def exec(instance: system.Instance, command: tuple[str, ...]) -> None:
    """Execute given PostgreSQL command in the libpq environment for `instance`.

    The command to be executed is looked up for in PostgreSQL binaries directory.
    """
    env = os.environ.copy()
    for key, value in env_for(instance).items():
        env.setdefault(key, value)
    progname, *args = command
    program = Path(progname)
    if not program.is_absolute():
        program = instance.postgresql.bindir / program
        if not program.exists():
            ppath = shutil.which(progname)
            if ppath is None:
                raise exceptions.FileNotFoundError(progname)
            program = Path(ppath)
    try:
        cmd.execute_program([str(program)] + args, env=env)
    except FileNotFoundError as e:
        raise exceptions.FileNotFoundError(str(e)) from e


def env(instance: system.Instance) -> str:
    return "\n".join(
        [
            f"export {key}={value}"
            for key, value in sorted(env_for(instance, path=True).items())
        ]
    )


def exists(name: str, version: str, settings: Settings) -> bool:
    """Return true when instance exists"""
    try:
        system.PostgreSQLInstance.system_lookup(name, version, settings)
    except exceptions.InstanceNotFound:
        return False
    return True


async def is_in_recovery(cnx: db.Connection) -> bool:
    """Return True if the instance is in recovery"""
    async with cnx.cursor(row_factory=psycopg.rows.args_row(bool)) as cur:
        await cur.execute("SELECT pg_is_in_recovery()")
        r = await cur.fetchone()
        assert r is not None
        return r


async def wait_recovery_finished(cnx: db.Connection, *, timeout: int = 10) -> None:
    logger.debug("checking if PostgreSQL is in recovery")
    async for attempt in AsyncRetrying(
        retry=retry_if_exception_type(exceptions.InstanceStateError),
        wait=wait_exponential(multiplier=1, min=1, max=timeout),
        stop=stop_after_delay(timeout),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        reraise=True,
    ):
        with attempt:
            if await is_in_recovery(cnx):
                raise exceptions.InstanceStateError("PostgreSQL still in recovery")


async def settings(cnx: db.Connection) -> list[system.PGSetting]:
    """Return the list of run-time parameters of the server, as available in
    pg_settings view.
    """
    async with cnx.cursor(row_factory=psycopg.rows.class_row(system.PGSetting)) as cur:
        await cur.execute(system.PGSetting.query)
        return await cur.fetchall()
