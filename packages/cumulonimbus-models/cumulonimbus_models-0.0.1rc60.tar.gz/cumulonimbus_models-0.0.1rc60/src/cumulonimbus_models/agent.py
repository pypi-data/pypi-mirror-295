from typing import ClassVar, Literal
from cumulonimbus_models.api import APIRequest
from cumulonimbus_models.base import Base


class AgentRegisterRequest(APIRequest):
    route_format: ClassVar[str] = '/agent/register'
    hostname: str


class AgentRegisterResponse(Base):
    agent_id: str
    agent_key: str
    ip_address: str
    operations_queue_url: str


class UnregisterAgentRequest(APIRequest):
    route_format: ClassVar[str] = '/agent/{agent_id}'


UnregisterAgentStatus = Literal['NOT_FOUND', 'SUCCESS']


class UnregisterAgentStatuses:
    NOT_FOUND: ClassVar[UnregisterAgentStatus] = 'NOT_FOUND'
    SUCCESS: ClassVar[UnregisterAgentStatus] = 'SUCCESS'


class UnregisterAgentResponse(Base):
    status: UnregisterAgentStatus

