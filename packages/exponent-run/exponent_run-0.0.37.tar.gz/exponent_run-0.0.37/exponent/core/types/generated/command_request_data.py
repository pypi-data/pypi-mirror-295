# Auto-generated, do not edit directly. Run `make generate_command_data` to update.

from enum import Enum
from typing import Literal

from pydantic import BaseModel


class CommandRequestType(str, Enum):
    FILE_READ = "file_read"
    FILE_OPEN = "file_open"


class CommandRequestData(BaseModel):
    pass


class FileReadCommandRequestData(CommandRequestData):
    type: Literal[CommandRequestType.FILE_READ] = CommandRequestType.FILE_READ

    file_path: str
    language: str


class FileOpenCommandRequestData(CommandRequestData):
    type: Literal[CommandRequestType.FILE_OPEN] = CommandRequestType.FILE_OPEN

    file_path: str
    language: str


CommandRequestDataType = FileReadCommandRequestData | FileOpenCommandRequestData
