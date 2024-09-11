# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Mapping, MutableMapping
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, TypeVar, Union

import psycopg.conninfo
from pgtoolkit import conf as pgconf
from pydantic import (
    AfterValidator,
    BeforeValidator,
    Field,
    PostgresDsn,
    SecretStr,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    ValidationInfo,
    WrapSerializer,
    model_validator,
)

from .. import conf, postgresql, types
from .. import settings as s
from .._compat import Self, assert_never
from ..annotations import ansible, cli
from ..pm import PluginManager
from ..postgresql import Standby
from ..settings import _postgresql as pgs
from ..settings import default_postgresql_version
from ..types import (
    BaseModel,
    ByteSize,
    CompositeModel,
    Port,
    Service,
    Status,
)
from .helpers import check_conninfo, check_excludes


def as_dict(value: Union[str, dict[str, Any]], *, key: str = "name") -> dict[str, Any]:
    """Possibly wrap a str value as a dict with specified 'key'.

    >>> as_dict({"x": 1})
    {'x': 1}
    >>> as_dict("x")
    {'name': 'x'}
    >>> as_dict("x", key="foo")
    {'foo': 'x'}
    """
    if isinstance(value, str):
        return {key: value}
    return value


def serialize(
    value: Any,
    handler: SerializerFunctionWrapHandler,
    info: SerializationInfo,
    *,
    key: str = "name",
) -> Any:
    """Serialize a complex field

    >>> class Foo(BaseModel):
    ...     attr1: str = ""
    >>> class Bar(BaseModel):
    ...     foos: list[
    ...         Annotated[Foo, WrapSerializer(partial(serialize, key="attr1"))]
    ...     ] = []
    >>> bar = Bar(foos=[{"attr1": "blah"}, {"attr1": "truite"}])
    >>> bar.model_dump()
    {'foos': [{'attr1': 'blah'}, {'attr1': 'truite'}]}
    >>> bar.model_dump(mode="pretty")
    {'foos': ['blah', 'truite']}
    """
    if info.mode == "pretty":
        return getattr(value, key)
    return handler(value)


def validate_state_is_absent(
    value: Union[bool, str], info: ValidationInfo
) -> Union[bool, str]:
    """Make sure state is absent.

    >>> Role(name="bob", drop_owned=False).state
    'present'
    >>> r = Role(name="bob", drop_owned=True)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Role
    drop_owned
      Value error, drop_owned can not be set if state is not 'absent' [type=value_error, input_value=True, input_type=bool]
        ...

    >>> r = Role(name="bob", reassign_owned="postgres")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Role
    reassign_owned
      Value error, reassign_owned can not be set if state is not 'absent' [type=value_error, input_value='postgres', input_type=str]
        ...

    >>> r = Database(name="db1", force_drop=True)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    force_drop
      Value error, force_drop can not be set if state is not 'absent' [type=value_error, input_value=True, input_type=bool]
        ...
    """
    if value and info.data.get("state") != "absent":
        raise ValueError(f"{info.field_name} can not be set if state is not 'absent'")
    return value


InstanceState = Literal["stopped", "started", "absent", "restarted"]


def state_from_pg_status(status: Status) -> InstanceState:
    """Instance state from PostgreSQL status.

    >>> state_from_pg_status(Status.running)
    'started'
    >>> state_from_pg_status(Status.not_running)
    'stopped'
    """
    if status is Status.running:
        return "started"
    elif status is Status.not_running:
        return "stopped"
    assert_never(status)


class RoleProfile(BaseModel):
    """Associate a usage profile to a role in a database for a list of
    database schema.
    """

    kind: Annotated[
        Literal["read-only", "read-write"],
        Field(description="The kind of profile to attach to target role."),
    ]
    database: Annotated[
        str,
        Field(description="The database scoped by this profile."),
        cli.Option(),
    ]
    schemas: Annotated[
        list[str],
        Field(description="List of database schema scoped by this profile."),
        cli.Option(name="schema"),
    ] = ["public"]


PresenceState = Literal["present", "absent"]


def check_mutually_exclusive_with(
    other: str,
    value: Optional[SecretStr],
    info: ValidationInfo,
    *,
    operations: Optional[set[types.Operation]] = None,
) -> Optional[SecretStr]:
    """Make sure currently validated field is not specified along with 'other' field.

    If 'operations' is set, the check will happen only if the 'operation' from
    validation context matches one of specified values.

    >>> class Foo(BaseModel):
    ...     bar: str = ""
    ...     dude: Annotated[
    ...         str, AfterValidator(partial(check_mutually_exclusive_with, "bar"))
    ...     ] = ""
    ...     baz: Annotated[
    ...         str,
    ...         AfterValidator(
    ...             partial(check_mutually_exclusive_with, "bar", operations={"create"})
    ...         ),
    ...     ] = ""

    >>> Foo(bar="blah", dude="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    dude
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    >>> from ..types import validation_context

    >>> with validation_context(operation="update"):
    ...     Foo(bar="blah", dude="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    dude
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    >>> with validation_context(operation="update"):
    ...     Foo(bar="blah", baz="blah")
    Foo(bar='blah', dude='', baz='blah')

    >>> with validation_context(operation="create"):
    ...     Foo(bar="blah", baz="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    baz
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    Without a validation context, no validation happens:
    >>> Foo(bar="blah", baz="blah")
    Foo(bar='blah', dude='', baz='blah')

    >>> Foo(bar="blah")
    Foo(bar='blah', dude='', baz='')
    """
    if (
        value
        and info.data.get(other)
        and (
            operations is None
            or (info.context is not None and info.context["operation"] in operations)
        )
    ):
        raise ValueError(f"field is mutually exclusive with {other!r}")
    return value


class BaseRole(CompositeModel):
    name: Annotated[
        str, Field(description="Role name.", json_schema_extra={"readOnly": True})
    ]
    state: Annotated[
        PresenceState,
        Field(
            description="Whether the role be present or absent.",
            exclude=True,
        ),
    ] = "present"
    password: Annotated[
        Optional[SecretStr], Field(description="Role password.", exclude=True)
    ] = None
    encrypted_password: Annotated[
        Optional[SecretStr],
        Field(description="Role password, already encrypted.", exclude=True),
        AfterValidator(partial(check_mutually_exclusive_with, "password")),
    ] = None

    @classmethod
    def component_models(cls, pm: PluginManager) -> list[types.ComponentModel]:
        return pm.hook.role_model()  # type: ignore[no-any-return]


DropOwned = Field(
    description="Drop all PostgreSQL's objects owned by the role being dropped.",
    exclude=True,
)
ReassignOwned = Field(
    description="Reassign all PostgreSQL's objects owned by the role being dropped to the specified role name.",
    min_length=1,
    exclude=True,
)


class RoleDropped(BaseRole):
    """Model for a role that is being dropped."""

    state: Literal["absent"] = "absent"
    password: Literal[None] = None
    encrypted_password: Literal[None] = None
    drop_owned: Annotated[bool, DropOwned] = False
    reassign_owned: Annotated[
        Optional[str],
        ReassignOwned,
        AfterValidator(partial(check_mutually_exclusive_with, "drop_owned")),
    ] = None


def _set_has_password(value: bool, info: ValidationInfo) -> bool:
    """Set 'has_password' field according to 'password'.

    >>> r = Role(name="postgres")
    >>> r.has_password
    False
    >>> r = Role(name="postgres", password="P4zzw0rd")
    >>> r.has_password
    True
    >>> r = Role(name="postgres", has_password=True)
    >>> r.has_password
    True
    """
    return (
        value
        or info.data["password"] is not None
        or info.data["encrypted_password"] is not None
    )


class RoleMembership(BaseModel):
    role: Annotated[
        str, Field(description="Role name.", json_schema_extra={"readOnly": True})
    ]

    state: Annotated[
        PresenceState,
        Field(
            description="Membership state. 'present' for 'granted', 'absent' for 'revoked'.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"


class _RoleExisting(BaseRole):
    """Base model for a role that exists (or should exist, after creation)."""

    has_password: Annotated[
        bool,
        cli.HIDDEN,
        ansible.HIDDEN,
        Field(
            description="True if the role has a password.",
            validate_default=True,
            json_schema_extra={"readOnly": True},
        ),
        AfterValidator(_set_has_password),
    ] = False
    inherit: Annotated[
        bool,
        Field(
            description="Let the role inherit the privileges of the roles it is a member of.",
        ),
    ] = True
    login: Annotated[bool, Field(description="Allow the role to log in.")] = False
    superuser: Annotated[
        bool, Field(description="Whether the role is a superuser.")
    ] = False
    createdb: Annotated[
        bool, Field(description="Whether role can create new databases.")
    ] = False
    createrole: Annotated[
        bool, Field(description="Whether role can create new roles.")
    ] = False
    replication: Annotated[
        bool, Field(description="Whether the role is a replication role.")
    ] = False
    connection_limit: Annotated[
        Optional[int],
        Field(description="How many concurrent connections the role can make."),
    ] = None
    validity: Annotated[
        Optional[datetime],
        Field(
            description="Date and time after which the role's password is no longer valid."
        ),
    ] = None
    memberships: Annotated[
        list[
            Annotated[
                RoleMembership,
                BeforeValidator(partial(as_dict, key="role")),
                WrapSerializer(partial(serialize, key="role")),
            ]
        ],
        cli.ListOption(
            name="in_role",
            metavar="role",
            item_key="role",
            names={"add": "--grant", "remove": "--revoke"},
            descriptions={
                "add": "Grant membership of the given role.",
                "remove": "Revoke membership of the given role.",
            },
        ),
        Field(description="Roles which this role should be a member of."),
    ] = []
    in_roles: Annotated[
        list[str],
        cli.HIDDEN,
        Field(description="DEPRECATED. Use 'memberships' instead."),
        AfterValidator(
            partial(
                check_mutually_exclusive_with,
                "memberships",
                operations={"create", "update"},
            )
        ),
    ] = []
    state: Annotated[
        PresenceState,
        cli.HIDDEN,
        Field(
            description="Whether the role be present or absent.",
            exclude=True,
        ),
    ] = "present"


class Role(_RoleExisting, RoleDropped):
    """PostgreSQL role"""

    drop_owned: Annotated[
        bool, DropOwned, cli.HIDDEN, AfterValidator(validate_state_is_absent)
    ] = False
    reassign_owned: Annotated[
        Optional[str],
        ReassignOwned,
        cli.HIDDEN,
        AfterValidator(validate_state_is_absent),
    ] = None


class Tablespace(BaseModel):
    name: str
    location: str
    size: ByteSize


class DatabaseListItem(BaseModel):
    name: str
    owner: str
    encoding: str
    collation: str
    ctype: str
    acls: list[str]
    size: ByteSize
    description: Optional[str]
    tablespace: Tablespace

    @classmethod
    def build(
        cls,
        *,
        tablespace: str,
        tablespace_location: str,
        tablespace_size: int,
        **kwargs: Any,
    ) -> Self:
        tblspc = Tablespace(
            name=tablespace, location=tablespace_location, size=tablespace_size
        )
        return cls(tablespace=tblspc, **kwargs)


class BaseDatabase(BaseModel):
    name: Annotated[
        str,
        Field(
            description="Database name.",
            json_schema_extra={"readOnly": True, "examples": ["demo"]},
        ),
    ]


ForceDrop = Field(description="Force the drop.", exclude=True)


class DatabaseDropped(BaseDatabase):
    """Model for a database that is being dropped."""

    force_drop: Annotated[bool, ForceDrop, cli.Option(name="force")] = False


class Schema(BaseModel):
    name: Annotated[
        str, Field(description="Schema name.", json_schema_extra={"readOnly": True})
    ]

    state: Annotated[
        PresenceState,
        Field(
            description="Schema state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"

    owner: Annotated[
        Optional[str],
        Field(
            description="The role name of the user who will own the schema.",
            json_schema_extra={"examples": ["postgres"]},
        ),
    ] = None


class Extension(BaseModel, frozen=True):
    name: Annotated[
        str, Field(description="Extension name.", json_schema_extra={"readOnly": True})
    ]
    schema_: Annotated[
        Optional[str],
        Field(
            alias="schema",
            description="Name of the schema in which to install the extension's object.",
        ),
    ] = None
    version: Annotated[
        Optional[str], Field(description="Version of the extension to install.")
    ] = None

    state: Annotated[
        PresenceState,
        Field(
            description="Extension state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"


class Publication(BaseModel):
    name: Annotated[
        str,
        Field(
            description="Name of the publication, unique in the database.",
        ),
    ]
    state: Annotated[
        PresenceState,
        Field(
            description="Presence state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"


class ConnectionString(BaseModel):
    conninfo: Annotated[
        str,
        Field(
            description="The libpq connection string, without password.",
        ),
        AfterValidator(partial(check_conninfo, exclude=[("password", "a password")])),
    ]
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Optional password to inject into the connection string.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    @classmethod
    def parse(cls, value: str) -> Self:
        conninfo = psycopg.conninfo.conninfo_to_dict(value)
        password = conninfo.pop("password", None)
        return cls(
            conninfo=psycopg.conninfo.make_conninfo("", **conninfo), password=password
        )

    @property
    def full_conninfo(self) -> str:
        """The full connection string, including password field."""
        password = None
        if self.password:
            password = self.password.get_secret_value()
        return psycopg.conninfo.make_conninfo(self.conninfo, password=password)


class Subscription(BaseModel):
    name: Annotated[str, Field(description="Name of the subscription.")]
    connection: Annotated[
        ConnectionString,
        Field(
            description="The libpq connection string defining how to connect to the publisher database.",
            json_schema_extra={"readOnly": True},
        ),
    ]
    publications: Annotated[
        list[str],
        Field(
            description="Publications on the publisher to subscribe to.",
            min_length=1,
        ),
    ]
    enabled: Annotated[
        bool, Field(description="Enable or disable the subscription.")
    ] = True
    state: Annotated[
        PresenceState,
        Field(
            description="Presence state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"

    @classmethod
    def from_row(cls, **kwargs: Any) -> Self:
        return cls(
            connection=ConnectionString.parse(kwargs.pop("connection")), **kwargs
        )


class CloneOptions(BaseModel):
    dsn: Annotated[
        PostgresDsn,
        cli.Argument(name="from", metavar="conninfo"),
        Field(
            description="Data source name of the database to restore into this one, specified as a libpq connection URI.",
        ),
    ]
    schema_only: Annotated[
        bool,
        Field(
            description="Only restore the schema (data definitions).",
        ),
    ] = False


def check_tablespace(value: str) -> Optional[str]:
    """Make sure tablespace is valid (ie. forbid 'default' or 'DEFAULT')

    >>> Database(name="x", tablespace="xyz")
    Database(name='x', force_drop=False, state='present', owner=None, settings=None, schemas=[], extensions=[], publications=[], subscriptions=[], clone=None, tablespace='xyz')
    >>> Database(name="x", tablespace="default")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    tablespace
      Value error, 'default' is not a valid value for 'tablespace'. Don't provide a value if you want the tablespace to be set to DEFAULT. [type=value_error, input_value='default', input_type=str]
        ...
    >>> Database(name="x", tablespace="DEFAULT")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Database
    tablespace
      Value error, 'DEFAULT' is not a valid value for 'tablespace'. Don't provide a value if you want the tablespace to be set to DEFAULT. [type=value_error, input_value='DEFAULT', input_type=str]
        ...
    """
    if value and value.lower() == "default":
        raise ValueError(
            f"{value!r} is not a valid value for 'tablespace'. "
            "Don't provide a value if you want the tablespace to be set to DEFAULT."
        )
    return value


class Database(DatabaseDropped):
    """PostgreSQL database"""

    state: Annotated[
        PresenceState,
        cli.HIDDEN,
        Field(
            description="Database state.",
            exclude=True,
            json_schema_extra={"examples": ["present"]},
        ),
    ] = "present"
    owner: Annotated[
        Optional[str],
        Field(
            description="The role name of the user who will own the database.",
            json_schema_extra={"examples": ["postgres"]},
        ),
    ] = None
    settings: Annotated[
        Optional[MutableMapping[str, Optional[pgconf.Value]]],
        cli.HIDDEN,
        ansible.Spec(spec={"type": "dict", "required": False}),
        Field(
            description=(
                "Session defaults for run-time configuration variables for the database. "
                "Upon update, an empty (dict) value would reset all settings."
            ),
            json_schema_extra={"examples": [{"work_mem": "5MB"}]},
        ),
    ] = None
    schemas: Annotated[
        list[
            Annotated[
                Schema,
                BeforeValidator(as_dict),
                WrapSerializer(serialize),
            ]
        ],
        cli.ListOption(
            name="schema",
            descriptions={
                "add": "Schemas to add to this database.",
                "remove": "Schemas to remove from this database.",
            },
        ),
        Field(
            description="Schemas in this database.",
            json_schema_extra={"examples": [{"name": "sales"}, "accounting"]},
        ),
    ] = []
    extensions: Annotated[
        list[
            Annotated[
                Extension,
                BeforeValidator(as_dict),
                WrapSerializer(serialize),
            ]
        ],
        cli.ListOption(
            name="extension",
            descriptions={
                "add": "Extensions to add to this database.",
                "remove": "Extensions to remove from this database.",
            },
        ),
        Field(
            description="Extensions in this database.",
            json_schema_extra={
                "examples": [
                    {"name": "unaccent", "schema": "ext", "version": "1.0"},
                    "hstore",
                ]
            },
        ),
    ] = []

    publications: Annotated[
        list[Publication],
        cli.HIDDEN,
        Field(
            description="Publications in this database.",
            json_schema_extra={"examples": [{"name": "mypub"}]},
        ),
    ] = []

    subscriptions: Annotated[
        list[Subscription],
        cli.HIDDEN,
        Field(
            description="Subscriptions in this database.",
            json_schema_extra={
                "examples": [
                    {"name": "mysub", "publications": ["mypub"], "enabled": False},
                ]
            },
        ),
    ] = []

    clone: Annotated[
        Optional[CloneOptions],
        Field(
            description="Options for cloning a database into this one.",
            exclude=True,
            json_schema_extra={
                "readOnly": True,
                "writeOnly": True,
                "examples": [
                    "postgresql://app:password@dbserver:5455/appdb",
                    {
                        "dsn": "postgresql://app:password@dbserver:5455/appdb",
                        "schema_only": True,
                    },
                ],
            },
        ),
    ] = None

    tablespace: Annotated[
        Optional[str],
        Field(
            description="The name of the tablespace that will be associated with the database.",
        ),
        AfterValidator(check_tablespace),
    ] = None

    force_drop: Annotated[
        bool, ForceDrop, cli.HIDDEN, AfterValidator(validate_state_is_absent)
    ] = False

    @model_validator(mode="after")
    def __set_schemas_owner_(self) -> Self:
        """Set schemas owner to that of the database, unless explicitly specified."""
        if self.owner is not None:
            for idx, schema in enumerate(self.schemas):
                if schema.owner is None:
                    self.schemas[idx] = schema.model_copy(update={"owner": self.owner})
        return self


def _sort(value: list[str]) -> list[str]:
    value.sort()
    return value


def _sort_values(value: dict[str, list[str]]) -> dict[str, list[str]]:
    for v in value.values():
        v.sort()
    return value


class DefaultPrivilege(BaseModel):
    """Default access privilege"""

    database: str
    schema_: Annotated[str, Field(alias="schema")]
    object_type: str
    role: str
    privileges: Annotated[list[str], AfterValidator(_sort)]


class Privilege(DefaultPrivilege):
    """Access privilege"""

    object_name: str
    column_privileges: Annotated[Mapping[str, list[str]], AfterValidator(_sort_values)]


class Auth(types.BaseModel):
    local: Annotated[
        Optional[pgs.AuthLocalMethods],
        Field(
            description="Authentication method for local-socket connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    host: Annotated[
        Optional[pgs.AuthHostMethods],
        Field(
            description="Authentication method for local TCP/IP connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    hostssl: Annotated[
        Optional[pgs.AuthHostSSLMethods],
        Field(
            description="Authentication method for SSL-encrypted TCP/IP connections",
            json_schema_extra={"readOnly": True},
        ),
    ] = None


class InstanceRef(BaseModel):
    """The minimal model for an existing instance."""

    name: Annotated[str, Field(description="Instance name.")]
    version: Annotated[str, Field(description="PostgreSQL version.")]
    port: Annotated[
        int, Field(description="TCP port the PostgreSQL instance is listening to.")
    ]
    datadir: Annotated[Path, Field(description="PostgreSQL data directory.")]


class InstanceListItem(InstanceRef):
    status: Annotated[str, Field(description="Runtime status.")]


def _default_version(value: Any, info: ValidationInfo) -> Any:
    if value is None:
        assert info.context, f"cannot validate {info.field_name} without a context"
        settings = info.context["settings"]
        return default_postgresql_version(settings.postgresql)
    return value


def _no_port_in_settings(value: dict[str, Any]) -> dict[str, Any]:
    if "port" in value:
        raise ValueError("'port' entry is disallowed; use the main 'port' field")
    return value


def _port_unset_is_available(
    value: Optional[Port], info: ValidationInfo
) -> Optional[Port]:
    """Check availability of the 'port' if the field is unset and its value
    would be picked from site template or the default 5432.
    """
    if value is None:
        template = postgresql.template(info.data["version"], "postgresql.conf")
        config = pgconf.parse_string(template)
        types.check_port_available(conf.get_port(config), info)
    return value


def _postgresql_auth_options(auth: Optional[Auth], settings: pgs.AuthSettings) -> Auth:
    local, host, hostssl = settings.local, settings.host, settings.hostssl
    if auth:
        local = auth.local or local
        host = auth.host or host
        hostssl = auth.hostssl or hostssl
    return Auth(local=local, host=host, hostssl=hostssl)


def _password_required_for_local_auth(
    value: Optional[SecretStr], info: ValidationInfo
) -> Optional[SecretStr]:
    """Validate that 'value' is not None if local auth method requires a
    password.
    """
    if (
        value is None
        and info.context
        and info.context.get("operation") == "create"
        and info.data.get("state") != "absent"
        and not info.data.get("upgrading_from")
    ):
        settings = info.context["settings"].postgresql
        assert info.field_name is not None
        auth = _postgresql_auth_options(info.data["auth"], settings.auth)
        if auth.local in ("password", "md5", "scram-sha-256"):
            raise ValueError(
                f"a value is required per local authentication method {auth.local!r}"
            )
    return value


class Instance(CompositeModel):
    """A pglift instance, on top of a PostgreSQL instance.

    This combines the definition of a base PostgreSQL instance with extra
    satellite components.

    When unspecified, some fields values are computed from site settings and
    site templates, the combination of which serves as a default "template"
    for the Instance model.

    >>> Instance(name="without_dash", version="15")  # doctest: +ELLIPSIS
    Instance(name='without_dash', ...)
    >>> Instance(name="with-dash", version="15")
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
    name
      Value error, must not contain dashes [type=value_error, input_value='with-dash', input_type=str]
      ...
    >>> Instance(name="with/slash", version="15")
    Traceback (most recent call last):
        ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Instance
    name
      Value error, must not contain slashes [type=value_error, input_value='with/slash', input_type=str]
      ...
    """

    @classmethod
    def component_models(cls, pm: PluginManager) -> list[types.ComponentModel]:
        return pm.hook.instance_model()  # type: ignore[no-any-return]

    name: Annotated[
        str,
        Field(description="Instance name.", json_schema_extra={"readOnly": True}),
        AfterValidator(partial(check_excludes, ("/", "slashes"))),
        AfterValidator(partial(check_excludes, ("-", "dashes"))),
    ]
    version: Annotated[
        pgs.PostgreSQLVersion,
        Field(
            default=None,
            description="PostgreSQL version; if unspecified, determined from site settings or most recent PostgreSQL installation available on site.",
            json_schema_extra={"readOnly": True},
            validate_default=True,
        ),
        BeforeValidator(_default_version),
    ]

    state: Annotated[
        InstanceState,
        cli.Choices(choices=["started", "stopped"]),
        Field(description="Runtime state."),
    ] = "started"

    standby: Annotated[
        Optional[Standby],
        Field(description="Standby information."),
    ] = None

    upgrading_from: Annotated[
        Optional[InstanceRef],
        cli.HIDDEN,
        ansible.HIDDEN,
        Field(
            description="Internal field to keep a reference to the instance this manifest will be upgraded from.",
            exclude=True,
        ),
    ] = None

    port: Annotated[
        Optional[Port],
        AfterValidator(_port_unset_is_available),
        Field(
            description="TCP port the PostgreSQL instance will be listening to.",
            validate_default=True,
        ),
    ] = None
    settings: Annotated[
        MutableMapping[str, Any],
        AfterValidator(_no_port_in_settings),
        cli.HIDDEN,
        Field(
            description=("Settings for the PostgreSQL instance."),
            json_schema_extra={
                "examples": [
                    {
                        "listen_addresses": "*",
                        "shared_buffers": "1GB",
                        "ssl": True,
                        "ssl_key_file": "/etc/certs/db.key",
                        "ssl_cert_file": "/etc/certs/db.key",
                        "shared_preload_libraries": "pg_stat_statements",
                    }
                ]
            },
        ),
    ] = {}

    data_checksums: Annotated[
        Optional[bool],
        Field(
            description=(
                "Enable or disable data checksums. "
                "If unspecified, fall back to site settings choice."
            ),
        ),
    ] = None
    locale: Annotated[
        Optional[str],
        Field(
            description="Default locale.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None
    encoding: Annotated[
        Optional[str],
        Field(
            description="Character encoding of the PostgreSQL instance.",
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    auth: Annotated[
        Optional[Auth], Field(exclude=True, json_schema_extra={"writeOnly": True})
    ] = None

    surole_password: Annotated[
        Optional[SecretStr],
        cli.Option(metavar="password"),
        AfterValidator(_password_required_for_local_auth),
        Field(
            description="Super-user role password.",
            exclude=True,
            validate_default=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    replrole_password: Annotated[
        Optional[SecretStr],
        cli.Option(metavar="password"),
        Field(
            description="Replication role password.",
            exclude=True,
            json_schema_extra={"readOnly": True},
        ),
    ] = None

    databases: Annotated[
        list[Database],
        cli.HIDDEN,
        Field(
            description="Databases defined in this instance (non-exhaustive list).",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = []
    roles: Annotated[
        list[Role],
        cli.HIDDEN,
        Field(
            description="Roles defined in this instance (non-exhaustive list).",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = []

    pending_restart: Annotated[
        bool,
        cli.HIDDEN,
        ansible.HIDDEN,
        Field(
            description="Whether the instance needs a restart to account for settings changes.",
            json_schema_extra={"readOnly": True},
        ),
    ] = False
    restart_on_changes: Annotated[
        bool,
        cli.HIDDEN,
        Field(
            description="Whether or not to automatically restart the instance to account for settings changes.",
            exclude=True,
            json_schema_extra={"writeOnly": True},
        ),
    ] = False

    @model_validator(mode="before")
    @classmethod
    def __validate_standby_and_patroni_(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values.get("standby") and values.get("patroni"):
            raise ValueError("'patroni' and 'standby' fields are mutually exclusive")
        return values

    _S = TypeVar("_S", bound=Service)

    def service(self, stype: type[_S]) -> _S:
        """Return satellite Service attached to this instance.

        :raises ValueError: if not found.
        """
        fname = stype.__service__
        try:
            s = getattr(self, fname)
        except AttributeError as e:
            raise ValueError(fname) from e
        if s is None:
            raise ValueError(fname)
        assert isinstance(
            s, stype
        ), f"expecting field {fname} to have type {stype} (got {type(s)})"
        return s

    def surole(self, settings: s.Settings) -> Role:
        s = settings.postgresql.surole
        extra = {}
        if settings.postgresql.auth.passfile is not None:
            extra["pgpass"] = s.pgpass
        return Role(name=s.name, password=self.surole_password, **extra)

    def replrole(self, settings: s.Settings) -> Optional[Role]:
        if (name := settings.postgresql.replrole) is None:
            return None
        return Role(
            name=name,
            password=self.replrole_password,
            login=True,
            replication=True,
            memberships=["pg_read_all_stats"],
        )

    def auth_options(self, settings: pgs.AuthSettings) -> Auth:
        return _postgresql_auth_options(self.auth, settings)

    def pg_hba(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        auth = self.auth_options(settings.postgresql.auth)
        return postgresql.template(self.version, "pg_hba.conf").format(
            auth=auth,
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
        )

    def pg_ident(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        return postgresql.template(self.version, "pg_ident.conf").format(
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
            sysuser=settings.sysuser[0],
        )

    def initdb_options(self, base: pgs.InitdbSettings) -> pgs.InitdbSettings:
        data_checksums: Union[None, Literal[True]] = {
            True: True,
            False: None,
            None: base.data_checksums or None,
        }[self.data_checksums]
        return pgs.InitdbSettings(
            locale=self.locale or base.locale,
            encoding=self.encoding or base.encoding,
            data_checksums=data_checksums,
        )


class ApplyResult(BaseModel):
    """
    ApplyResult allows to describe the result of a call to apply function
    (Eg: pglift.database.apply) to an object (Eg: database, instance,...).

    The `change_state` attribute of this class can be set to one of to those values:
      - `'created'` if the object has been created,
      - `'changed'` if the object has been changed,
      - `'dropped'` if the object has been dropped,
      - :obj:`None` if nothing happened to the object we manipulate (neither created,
        changed or dropped)
    """

    change_state: Annotated[
        Optional[Literal["created", "changed", "dropped"]],
        Field(
            description="Define the change applied (created, changed or dropped) to a manipulated object",
        ),
    ] = None  #:


class InstanceApplyResult(ApplyResult):
    pending_restart: Annotated[
        bool,
        Field(
            description="Whether the instance needs a restart to account for settings changes.",
        ),
    ] = False
