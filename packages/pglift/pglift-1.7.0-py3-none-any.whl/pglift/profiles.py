# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from psycopg import sql

from . import databases, db, schemas
from .models import interface, system

logger = logging.getLogger(__name__)


async def _define_grantor(
    cnx: db.Connection, instance: system.PostgreSQLInstance, database: str, schema: str
) -> str:
    """Define grantor (role used behind FOR ROLE when altering default privileges)
    based on schema owner or database owner if the schema is owned by the pre-defined
    role pg_database_owner (default value for the public schema on PostgreSQL>=14).
    """
    schema_owner = await schemas.owner(cnx, schema=schema)
    if schema_owner != "pg_database_owner":
        return schema_owner
    db_owner = (await databases.get(instance, database)).owner
    assert db_owner
    return db_owner


async def revoke(
    cnx: db.Connection,
    instance: system.PostgreSQLInstance,
    role: str,
    database: str,
    schema: str,
) -> None:
    """Revoke all privileges for a PostgreSQL role for a specific database and
    schema.
    """
    grantor = await _define_grantor(cnx, instance, database, schema)
    for stmt in db.queries(
        "profile_reset",
        dbname=sql.Identifier(database),
        username=sql.Identifier(role),
        grantor=sql.Identifier(grantor),
        schemaname=sql.Identifier(schema),
    ):
        await cnx.execute(stmt)


async def set_for_role(
    instance: system.PostgreSQLInstance, role: str, profile: interface.RoleProfile
) -> None:
    """Alter privileges to ensure a role has profile based privileges.

    First removes / revokes all privileges for the role (database and schema)
    and then applies the PostgreSQL commands (mainly GRANT and ALTER DEFAULT
    PRIVILEGES) based on the profile definition.
    """
    async with db.connect(instance, dbname=profile.database) as cnx, cnx.transaction():
        for s in profile.schemas:
            grantor = await _define_grantor(cnx, instance, profile.database, s)
            async with cnx.transaction():
                await revoke(cnx, instance, role, profile.database, s)
                logger.info(
                    "setting profile '%(profile)s' for role '%(role)s' on schema '%(schema)s' in database '%(database)s'",
                    {
                        "profile": profile.kind,
                        "role": role,
                        "schema": s,
                        "database": profile.database,
                    },
                )
                for stmt in db.queries(
                    f"profile_{profile.kind}",
                    schemaname=sql.Identifier(s),
                    grantor=sql.Identifier(grantor),
                    username=sql.Identifier(role),
                ):
                    await cnx.execute(stmt)
