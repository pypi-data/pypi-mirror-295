# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated, Final, Optional

from pydantic import Field, SecretStr

from ... import types

default_port: Final = 2345


class Service(types.Service, service_name="temboard"):
    port: Annotated[
        types.Port,
        Field(
            description="TCP port for the temboard-agent API.",
            validate_default=True,
        ),
    ] = default_port
    password: Annotated[
        Optional[SecretStr],
        Field(
            description="Password of PostgreSQL role for temboard agent.",
            exclude=True,
        ),
    ] = None
