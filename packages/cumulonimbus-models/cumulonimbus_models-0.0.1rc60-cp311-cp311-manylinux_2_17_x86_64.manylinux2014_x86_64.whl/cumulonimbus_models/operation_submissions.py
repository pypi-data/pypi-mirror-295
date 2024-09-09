import collections
from typing import ClassVar
from cumulonimbus_models.base import Base
from cumulonimbus_models.operations import OperationTypes, OperationType, SubmitOperationRequest


class SubmitUpdateOperationRequest(SubmitOperationRequest):
    type: ClassVar[OperationType] = OperationTypes.UPDATE
    parameters: dict[str, str] = {}


class ShellCommandOperationParameters(Base):
    command: str
    args: list[str] = []


class SubmitShellCommandOperationRequest(SubmitOperationRequest):
    type: ClassVar[OperationType] = OperationTypes.SHELL_COMMAND
    parameters: ShellCommandOperationParameters

