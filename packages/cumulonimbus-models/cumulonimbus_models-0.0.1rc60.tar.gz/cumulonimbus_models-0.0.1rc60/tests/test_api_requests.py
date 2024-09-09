import pytest


from cumulonimbus_models.agent import AgentRegisterRequest,  UnregisterAgentRequest
from cumulonimbus_models.operations import SubmitOperationRequest, UpdateOperationResultRequest
from cumulonimbus_models.system import SystemUpdateRequest
from cumulonimbus_models.api import APIRequest


@pytest.mark.parametrize('req_type', [AgentRegisterRequest,  UnregisterAgentRequest, SubmitOperationRequest, UpdateOperationResultRequest, SystemUpdateRequest, APIRequest])
def test_api_requests(req_type: type):
    req_type.route()
    req_type.get_url({k: 'test' for k in req_type.format_args()})


def test_get_url():
    APIRequest().get_url()


def test_fail_get_url_invalid_argument():
    invalid_arg = 'a'
    msg = f'Invalid argument: {invalid_arg}'
    with pytest.raises(ValueError, match=f"^{msg}$"):
        APIRequest().get_url({'a': None})


def test_fail_get_url_missing_args():
    missing_arg = 'agent_id'
    msg = '^Missing arguments: {'+f"'{missing_arg}'"+'}$'
    with pytest.raises(ValueError, match=msg):
        SubmitOperationRequest().get_url()
