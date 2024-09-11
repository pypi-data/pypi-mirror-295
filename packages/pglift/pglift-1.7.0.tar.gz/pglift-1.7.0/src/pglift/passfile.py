# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from copy import copy
from pathlib import Path
from typing import Annotated, TypedDict

from pgtoolkit import pgpass
from pgtoolkit.conf import Configuration
from pydantic import Field

from . import conf, hookimpl, types
from .models import interface, system
from .settings import Settings

logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    return settings.postgresql.auth.passfile is not None


def _passfile(settings: Settings) -> Path:
    passfile = settings.postgresql.auth.passfile
    assert passfile is not None  # per registration
    return passfile


@hookimpl
def role_model() -> types.ComponentModel:
    return types.ComponentModel(
        "pgpass",
        (
            Annotated[
                bool,
                Field(
                    description="Whether to add an entry in password file for this role.",
                ),
            ],
            False,
        ),
    )


@hookimpl
async def instance_configured(
    instance: system.PostgreSQLInstance,
    manifest: interface.Instance,
    config: Configuration,
    changes: types.ConfigChanges,
    creating: bool,
) -> None:
    """Update passfile entry for PostgreSQL roles upon instance
    re-configuration (port change).
    """
    if creating or "port" not in changes:
        return
    old_port, port = changes["port"]
    if port is None:
        port = conf.get_port(config)
    if old_port is None:
        old_port = 5432
    assert isinstance(old_port, int)
    assert isinstance(port, int), port
    if port == old_port:
        return

    passfile = _passfile(instance._settings)
    with pgpass.edit(passfile) as f:
        for entry in f:
            if entry.matches(port=old_port):
                entry.port = port
                logger.info(
                    "updating entry for '%(username)s' in %(passfile)s (port changed: %(old_port)d->%(port)d)",
                    {
                        "username": entry.username,
                        "passfile": passfile,
                        "old_port": old_port,
                        "port": port,
                    },
                )


@hookimpl
async def instance_dropped(instance: system.Instance) -> None:
    """Remove password file (pgpass) entries for the instance being dropped."""
    passfile_path = _passfile(instance._settings)
    if not passfile_path.exists():
        return
    port = instance.postgresql.port
    with pgpass.edit(passfile_path) as passfile:
        logger.info(
            "removing entries matching port=%(port)s from %(passfile)s",
            {"port": port, "passfile": passfile_path},
        )
        passfile.remove(port=port)
    if not passfile.lines:
        logger.info(
            "removing now empty %(passfile)s",
            {"passfile": passfile_path},
        )
        passfile_path.unlink()


@hookimpl
def instance_upgraded(
    old: system.PostgreSQLInstance, new: system.PostgreSQLInstance
) -> None:
    """Add pgpass entries matching 'old' instance for the 'new' one."""
    old_port = old.port
    new_port = new.port
    if new_port == old_port:
        return
    passfile = _passfile(old._settings)
    with pgpass.edit(passfile) as f:
        for entry in list(f):
            if entry.matches(port=old_port):
                new_entry = copy(entry)
                new_entry.port = new_port
                f.lines.append(new_entry)
                logger.info("added entry %s in %s", new_entry, passfile)


@hookimpl
def role_change(role: interface.BaseRole, instance: system.PostgreSQLInstance) -> bool:
    """Create / update or delete passfile entry matching ('role', 'instance')."""
    port = instance.port
    username = role.name
    password = None
    if role.password:
        password = role.password.get_secret_value()
    in_pgpass = getattr(role, "pgpass", False)
    passfile = _passfile(instance._settings)
    with pgpass.edit(passfile) as f:
        for entry in f:
            if entry.matches(username=username, port=port):
                if role.state == "absent" or not in_pgpass:
                    logger.info(
                        "removing entry for '%(username)s' in %(passfile)s (port=%(port)d)",
                        {"username": username, "passfile": passfile, "port": port},
                    )
                    f.lines.remove(entry)
                    return True
                elif password is not None and entry.password != password:
                    logger.info(
                        "updating password for '%(username)s' in %(passfile)s (port=%(port)d)",
                        {"username": username, "passfile": passfile, "port": port},
                    )
                    entry.password = password
                    return True
                return False
        else:
            if in_pgpass and password is not None:
                logger.info(
                    "adding an entry for '%(username)s' in %(passfile)s (port=%(port)d)",
                    {"username": username, "passfile": passfile, "port": port},
                )
                entry = pgpass.PassEntry("*", port, "*", username, password)
                f.lines.append(entry)
                f.sort()
                return True
            return False


class RoleInspect(TypedDict):
    pgpass: bool


@hookimpl
def role_inspect(instance: system.PostgreSQLInstance, name: str) -> RoleInspect:
    passfile_path = _passfile(instance._settings)
    if not passfile_path.exists():
        return {"pgpass": False}
    passfile = pgpass.parse(passfile_path)
    return {
        "pgpass": any(e.matches(username=name, port=instance.port) for e in passfile)
    }
