from typing import ClassVar, Literal


from cumulonimbus_models.api import APIRequest
from cumulonimbus_models.base import Base


SoftwareInstallationMethod = Literal[
    'PIP',
    'MANUAL',
    'APT',
    'GIT'
]


class SoftwareInstallationMethods:
    PIP: ClassVar[SoftwareInstallationMethod] = 'PIP'
    MANUAL: ClassVar[SoftwareInstallationMethod] = 'MANUAL'
    APT: ClassVar[SoftwareInstallationMethod] = 'APT'
    GIT: ClassVar[SoftwareInstallationMethod] = 'GIT'


class Software(Base):
    name: str
    version: str
    installation_method: SoftwareInstallationMethod
    installation_data: dict[str, str]
    config_data: dict[str, str]


class SystemInfo(Base):
    os: str
    hostname: str
    software: list[Software]


# noinspection PyMethodOverriding,PyUnusedClass
class SystemUpdateRequest(APIRequest):
    route_format: ClassVar[str] = '/agent/{agent_id}/system_update'
    system_info: SystemInfo

