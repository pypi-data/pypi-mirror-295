# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

import warnings
from pathlib import Path
from typing import Annotated, Any, Optional

from pydantic import AfterValidator, Field, ValidationInfo

from pglift.settings import Settings as BaseSettings
from pglift.settings import SiteSettings as BaseSiteSettings
from pglift.settings.base import BaseModel, LogPath, RunPath


def deprecated(value: Any, info: ValidationInfo) -> Any:
    if value is not None:
        warnings.warn(
            f"{info.field_name!r} setting is deprecated", FutureWarning, stacklevel=2
        )
    return value


class AuditSettings(BaseModel):
    """Settings for change operations auditing."""

    path: Annotated[
        Annotated[Path, LogPath],
        Field(description="Log file path"),
    ]
    log_format: Annotated[
        str,
        Field(description="Format for log messages"),
    ] = "%(levelname)-8s - %(asctime)s - %(name)s - %(message)s"
    date_format: Annotated[
        str,
        Field(description="Date format in log messages"),
    ] = "%Y-%m-%d %H:%M:%S"


class CLISettings(BaseModel):
    """Settings for pglift's command-line interface."""

    logpath: Annotated[
        Annotated[Optional[Path], LogPath],
        Field(
            description="Directory where temporary debug files from command executions will be stored (DEPRECATED).",
        ),
        AfterValidator(deprecated),
    ] = None

    log_format: Annotated[
        str, Field(description="Format for log messages when written to a file")
    ] = "%(asctime)s %(levelname)-8s %(name)s - %(message)s"

    date_format: Annotated[
        str, Field(description="Date format in log messages when written to a file")
    ] = "%Y-%m-%d %H:%M:%S"

    lock_file: Annotated[
        Path, RunPath, Field(description="Path to lock file dedicated to pglift")
    ] = Path(".pglift.lock")

    audit: Annotated[
        Optional[AuditSettings],
        Field(description="Settings for change operations auditing"),
    ] = None


class Settings(BaseSettings):
    cli: Annotated[CLISettings, Field(default_factory=CLISettings)]


class SiteSettings(Settings, BaseSiteSettings):
    pass
