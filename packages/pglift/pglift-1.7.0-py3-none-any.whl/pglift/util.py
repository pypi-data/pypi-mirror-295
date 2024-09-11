# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import shutil
import warnings
from pathlib import Path
from types import TracebackType
from typing import Any

import humanize

from . import __name__ as pkgname
from . import exceptions
from ._compat import read_resource

logger = logging.getLogger(__name__)


def environ() -> dict[str, str]:
    """Return the pglift-specific environment mapping."""
    prefix = pkgname.upper()
    return {k: v for k, v in os.environ.items() if k.startswith(f"{prefix}_")}


def template(bases: str | tuple[tuple[str, ...] | str, ...], *args: str) -> str:
    r"""Return the content of a configuration file template, either found in
    site configuration or in distribution data.

    :param bases: The base component(s) of the path where the template file
        will be looked for; may be a single string or a tuple of string-tuples
        describing alternative "bases" to look into.
    :param args: Final path components of the template file to look for.

    :return: The content of found template file.

    Examples:

    Look for 'postgresql/pg_hba.conf' in site configuration and then
    distribution data::

        >>> print(template("postgresql", "pg_hba.conf"))
        local   all             {surole}                                {auth.local}
        local   all             all                                     {auth.local}
        host    all             all             127.0.0.1/32            {auth.host}
        host    all             all             ::1/128                 {auth.host}
        <BLANKLINE>

    Look for 'postgresql.conf' template first in 'postgresql/16' directory in
    site configuration and fall back to 'postgresql/postgresql.conf' in
    distribution data::

        >>> print(template((("postgresql", "16"), "postgresql"), "postgresql.conf"))
        cluster_name = {name}
        shared_buffers = 25%
        effective_cache_size = 66%
        unix_socket_directories = {settings.socket_directory}
        log_directory = {settings.logpath}
        log_filename = '{version}-{name}-%Y-%m-%d_%H%M%S.log'
        log_destination = 'stderr'
        logging_collector = on
        <BLANKLINE>
    """
    file_content = read_site_config(bases, *args)
    assert file_content is not None
    return file_content


def etc() -> Path:
    return Path("/etc")


def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def xdg_runtime_dir(uid: int) -> Path:
    runtime_dir = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{uid}"))
    if runtime_dir.exists():
        return runtime_dir
    raise exceptions.FileNotFoundError(f"{runtime_dir} does not exist")


def etc_config(*parts: str) -> Path | None:
    """Return content of a configuration file in /etc."""
    config = (etc() / pkgname).joinpath(*parts)
    if config.exists():
        return config
    return None


def xdg_config(*parts: str) -> Path | None:
    """Return content of a configuration file in $XDG_CONFIG_HOME."""
    config = (xdg_config_home() / pkgname).joinpath(*parts)
    if config.exists():
        return config
    return None


def custom_config(*parts: str) -> Path | None:
    """Return content of a configuration file in $PGLIFT_CONFIG_DIR."""
    var = "PGLIFT_CONFIG_DIR"
    oldvar = "PGLIFT_CONFIG_PATH"
    if oldvar in os.environ:
        warnings.warn(
            f"{oldvar!r} environment variable is deprecated, use {var!r} instead",
            FutureWarning,
            stacklevel=1,
        )
        if var in os.environ:
            raise OSError(
                f"both {var!r} and {oldvar!r} environment variables are set (only the former should be used)"
            )
        var = oldvar
    if env := os.environ.get(var, None):
        path = Path(env)
        assert path.exists(), f"{env} (set via {var}) does not exist"
        config = path.joinpath(*parts)
        if config.exists():
            return config
    return None


def site_config(
    bases: str | tuple[tuple[str, ...] | str, ...], *args: str
) -> Path | None:
    """Lookup for a configuration file path in custom, user or site
    configuration.
    """
    if isinstance(bases, str):
        bases = (bases,)
    for bs in bases:
        if isinstance(bs, str):
            bs = (bs,)
        for hdlr in (custom_config, xdg_config, etc_config):
            if config := hdlr(*bs, *args):
                return config
    return None


def read_dist_config(*parts: str) -> str | None:
    """Return content of a configuration file in distribution resources."""
    subpkgs, resource_name = parts[:-1], parts[-1]
    pkg = ".".join([pkgname] + list(subpkgs))
    return read_resource(pkg, resource_name)


def read_site_config(
    bases: str | tuple[tuple[str, ...] | str, ...], *args: str
) -> str | None:
    """Return content of a configuration file looked-up in custom, user or
    site location, and fall back to distribution if not found.
    """
    if config := site_config(bases, *args):
        return config.read_text()
    if isinstance(bases, tuple):
        base = bases[-1]
        assert isinstance(base, str), f"expecting a string as last item of {bases}"
    else:
        base = bases
    return read_dist_config(base, *args)


def with_header(content: str, header: str) -> str:
    """Possibly insert `header` on top of `content`.

    >>> print(with_header("blah", "% head"))
    % head
    blah
    >>> with_header("content", "")
    'content'
    """
    if header:
        content = "\n".join([header, content])
    return content


def parse_filesize(value: str) -> float:
    """Parse a file size string as float, in bytes unit.

    >>> parse_filesize("6022056 kB")
    6166585344.0
    >>> parse_filesize("0")
    Traceback (most recent call last):
        ...
    ValueError: malformatted file size '0'
    >>> parse_filesize("5 km")
    Traceback (most recent call last):
        ...
    ValueError: invalid unit 'km'
    >>> parse_filesize("5 yb")
    Traceback (most recent call last):
        ...
    ValueError: invalid unit 'yb'
    """
    units = ["B", "K", "M", "G", "T"]
    try:
        val, unit = value.split(None, 1)
        mult, b = list(unit)
    except ValueError as e:
        raise ValueError(f"malformatted file size {value!r}") from e
    if b.lower() != "b":
        raise ValueError(f"invalid unit {unit!r}")
    try:
        scale = units.index(mult.upper())
    except ValueError as e:
        raise ValueError(f"invalid unit {unit!r}") from e
    assert isinstance(scale, int)
    return (1024**scale) * float(val)  # type: ignore[no-any-return]


def total_memory(path: Path = Path("/proc/meminfo")) -> float:  # noqa: B008
    """Read 'MemTotal' field from /proc/meminfo.

    :raise ~exceptions.SystemError: if reading the value failed.
    """
    with path.open() as meminfo:
        for line in meminfo:
            if not line.startswith("MemTotal:"):
                continue
            return parse_filesize(line.split(":", 1)[-1].strip())
        else:
            raise exceptions.SystemError(
                f"could not retrieve memory information from {path}"
            )


def percent_memory(value: str, total: float) -> str:
    """Convert 'value' from a percentage of total memory into a memory setting
    or return (as is if not a percentage value).

    >>> percent_memory(" 1GB", 1)
    '1GB'
    >>> percent_memory("25%", 4e9)
    '1 GB'
    >>> percent_memory("xyz%", 3e9)
    Traceback (most recent call last):
      ...
    ValueError: invalid percent value 'xyz'
    """
    value = value.strip()
    if value.endswith("%"):
        value = value[:-1].strip()
        try:
            percent_value = float(value) / 100
        except ValueError as e:
            raise ValueError(f"invalid percent value {value!r}") from e
        value = humanize.naturalsize(total * percent_value, format="%d")
    return value


def check_or_create_directory(path: Path, purpose: str, **kwargs: Any) -> None:
    """Ensure that 'path' directory is writable, or create it."""
    if path.exists():
        if not path.is_dir():
            raise exceptions.SystemError(f"{path} exists but is not a directory")
        if not os.access(path, os.W_OK):
            raise exceptions.SystemError(
                f"{purpose} directory {path} exists but is not writable"
            )
    else:
        logger.info("creating %s directory: %s", purpose, path)
        path.mkdir(parents=True, exist_ok=True, **kwargs)


def rmdir(path: Path) -> bool:
    """Try to remove 'path' directory, log a warning in case of failure,
    return True upon success.
    """
    try:
        path.rmdir()
        return True
    except OSError as e:
        logger.warning("failed to remove directory %s: %s", path, e)
        return False


def rmtree(path: Path, ignore_errors: bool = False) -> None:
    def log(
        func: Any,
        thispath: Any,
        exc_info: tuple[type[BaseException], BaseException, TracebackType],
    ) -> None:
        logger.warning(
            "failed to delete %s during tree deletion of %s: %s",
            thispath,
            path,
            exc_info[1],
        )

    shutil.rmtree(path, ignore_errors=ignore_errors, onerror=log)
