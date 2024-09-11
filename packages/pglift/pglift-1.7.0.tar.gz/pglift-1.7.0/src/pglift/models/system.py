# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, TypeVar

import psycopg.conninfo
import pydantic
from attrs import field, frozen
from attrs.validators import instance_of
from pgtoolkit.conf import Configuration

from .. import conf, exceptions, h, hooks
from .._compat import Self, datetime_fromisoformat
from ..settings import Settings, postgresql_datadir, postgresql_waldir
from ..settings._postgresql import PostgreSQLVersion


@frozen
class Standby:
    primary_conninfo: str
    slot: str | None
    password: pydantic.SecretStr | None

    @classmethod
    def system_lookup(cls, instance: PostgreSQLInstance) -> Self | None:
        standbyfile = (
            "standby.signal"
            if instance.version >= PostgreSQLVersion.v12
            else "recovery.conf"
        )
        if not (instance.datadir / standbyfile).exists():
            return None
        config = instance.config()
        try:
            dsn = config["primary_conninfo"]
        except KeyError:
            return None
        if not dsn:
            return None
        assert isinstance(dsn, str), dsn
        primary_conninfo = psycopg.conninfo.conninfo_to_dict(dsn)
        try:
            conn_password = primary_conninfo.pop("password")
        except KeyError:
            password = None
        else:
            assert isinstance(conn_password, str)
            password = pydantic.SecretStr(conn_password)
        slot = config.get("primary_slot_name")
        if slot is not None:
            assert isinstance(slot, str), slot
        return cls(
            primary_conninfo=psycopg.conninfo.make_conninfo("", **primary_conninfo),
            slot=slot or None,
            password=password,
        )


@frozen
class PostgreSQLInstance:
    """A bare PostgreSQL instance.

    :raises ~exceptions.InvalidVersion: if PostgreSQL executable directory
        (bindir) does not exist for specified version.
    """

    name: str
    version: PostgreSQLVersion = field(converter=PostgreSQLVersion, repr=str)

    _settings: Settings = field(validator=instance_of(Settings), repr=False)

    bindir: Path = field(init=False, repr=False)
    datadir: Path = field(init=False, repr=False)
    waldir: Path = field(init=False, repr=False)

    @bindir.default
    def _bindir_factory(self) -> Path:
        for v in self._settings.postgresql.versions:
            if self.version == v.version:
                return v.bindir
        raise exceptions.InvalidVersion(
            f"version {self.version} unsupported in site settings"
        )

    @datadir.default
    def _datadir_factory(self) -> Path:
        return postgresql_datadir(
            self._settings.postgresql, version=self.version, name=self.name
        )

    @waldir.default
    def _waldir_factory(self) -> Path:
        return postgresql_waldir(
            self._settings.postgresql, version=self.version, name=self.name
        )

    @classmethod
    @contextmanager
    def creating(cls, name: str, version: str, settings: Settings) -> Iterator[Self]:
        """Context manager to initialize a PostgreSQLInstance while deferring
        its "checks" at exit thus leaving the opportunity for actual creation
        and configuration tasks to run within the context.
        """
        self = cls(name, version, settings)
        yield self
        self.check()

    @classmethod
    def system_lookup(cls, name: str, version: str, settings: Settings) -> Self:
        """Build a PostgreSQLInstance by system lookup.

        :raises ~exceptions.InstanceNotFound: if the instance could not be
            found by system lookup.
        """
        try:
            self = cls(name, version, settings)
        except exceptions.InvalidVersion as e:
            raise exceptions.InstanceNotFound(f"{version}/{name}") from e
        self.check()
        return self

    @property
    def standby(self) -> Standby | None:
        return Standby.system_lookup(self)

    @classmethod
    def from_qualname(cls, value: str, settings: Settings) -> Self:
        """Lookup for an Instance by its qualified name."""
        try:
            version, name = value.split("-", 1)
        except ValueError:
            raise ValueError(f"invalid qualified name {value!r}") from None
        return cls.system_lookup(name, version, settings)

    def __str__(self) -> str:
        return f"{self.version}/{self.name}"

    @property
    def qualname(self) -> str:
        """Version qualified name, e.g. 13-main."""
        return f"{self.version}-{self.name}"

    def notfound(self, hint: str | None = None) -> exceptions.InstanceNotFound:
        return exceptions.InstanceNotFound(str(self), hint)

    def check(self) -> None:
        """Check if the instance exists and its configuration is valid.

        :raises ~exceptions.InvalidVersion: if PG_VERSION content does not
            match declared version
        :raises ~pglift.exceptions.InstanceNotFound: if PGDATA does not exist
        :raises ~pglift.exceptions.InstanceNotFound: if configuration cannot
            be read
        """
        if not self.datadir.exists():
            raise self.notfound("data directory does not exist")
        try:
            real_version = (self.datadir / "PG_VERSION").read_text().splitlines()[0]
        except FileNotFoundError:
            raise self.notfound("PG_VERSION file not found") from None
        if real_version != self.version:
            raise exceptions.InvalidVersion(
                f"version mismatch ({real_version} != {self.version})"
            )
        try:
            self.config()
        except FileNotFoundError as e:
            raise self.notfound(str(e)) from e

    def config(self, managed_only: bool = False) -> Configuration:
        """Return parsed PostgreSQL configuration for this instance.

        Refer to :func:`pglift.conf.read` for complete documentation.
        """
        try:
            return conf.read(self.datadir, managed_only=managed_only)
        except exceptions.FileNotFoundError:
            if managed_only:
                return Configuration()
            raise

    @property
    def port(self) -> int:
        """TCP port the server listens on."""
        return conf.get_port(self.config())

    @property
    def socket_directory(self) -> str | None:
        """Directory path in which the socket should be.

        This is determined from 'unix_socket_directories' configuration entry,
        only considering the first item not starting with @. None if that
        setting is not defined.
        """
        if value := self.config().get("unix_socket_directories"):
            assert isinstance(value, str)
            for sdir in value.split(","):
                sdir = sdir.strip()
                if not sdir.startswith("@"):
                    return sdir
        return None

    @property
    def dumps_directory(self) -> Path:
        """Path to directory where database dumps are stored."""
        return Path(
            str(self._settings.postgresql.dumps_directory).format(
                version=self.version, name=self.name
            )
        )

    @property
    def psqlrc(self) -> Path:
        return self.datadir / ".psqlrc"

    @property
    def psql_history(self) -> Path:
        return self.datadir / ".psql_history"


@frozen
class Instance:
    """A PostgreSQL instance with satellite services."""

    postgresql: PostgreSQLInstance
    name: str = field(init=False)
    services: list[Any] = field()

    _settings: Settings = field(init=False, validator=instance_of(Settings), repr=False)

    @name.default
    def _default_name(self) -> str:
        return self.postgresql.name

    @services.validator
    def _validate_services(self, attribute: Any, value: list[Any]) -> None:
        if len(set(map(type, value))) != len(value):
            raise ValueError("values for 'services' field must be of distinct types")

    @services.default
    def _build_services(self) -> list[Any]:
        postgresql = self.postgresql
        settings = postgresql._settings
        return [
            s
            for s in hooks(settings, h.system_lookup, instance=postgresql)
            if s is not None
        ]

    @_settings.default
    def __settings_from_postgresql_(self) -> Settings:
        return self.postgresql._settings

    @classmethod
    def system_lookup(cls, name: str, version: str, settings: Settings) -> Self:
        postgresql = PostgreSQLInstance.system_lookup(name, version, settings)
        return cls.from_postgresql(postgresql)

    @classmethod
    def from_postgresql(cls, postgresql: PostgreSQLInstance) -> Self:
        return cls(postgresql=postgresql)

    def __str__(self) -> str:
        return self.postgresql.__str__()

    @property
    def qualname(self) -> str:
        return self.postgresql.qualname

    S = TypeVar("S")

    def service(self, stype: type[S]) -> S:
        """Return bound satellite service object matching requested type.

        :raises ValueError: if not found.
        """
        for s in self.services:
            if isinstance(s, stype):
                return s
        raise ValueError(stype)


@frozen
class DatabaseDump:
    id: str
    dbname: str
    date: datetime = field(converter=datetime_fromisoformat)  # type: ignore[misc]
    path: Path

    @classmethod
    def from_path(cls, path: Path) -> Self | None:
        """Build a DatabaseDump from a dump file path or return None if file
        name does not match expected format.
        """
        try:
            dbname, date = path.stem.rsplit("_", 1)
        except ValueError:
            return None
        return cls.build(dbname, date, path)

    @classmethod
    def build(cls, dbname: str, date: str, path: Path) -> Self:
        """Build a DatabaseDump from dbname and date."""
        id = "_".join(
            [
                dbname,
                hashlib.blake2b(
                    (dbname + date).encode("utf-8"), digest_size=5
                ).hexdigest(),
            ]
        )
        return cls(id=id, dbname=dbname, date=date, path=path)


@frozen
class PGSetting:
    """A column from pg_settings view."""

    query: ClassVar[str] = (
        "SELECT name, setting, context, pending_restart FROM pg_settings"
    )

    name: str
    setting: str
    context: str
    pending_restart: bool
