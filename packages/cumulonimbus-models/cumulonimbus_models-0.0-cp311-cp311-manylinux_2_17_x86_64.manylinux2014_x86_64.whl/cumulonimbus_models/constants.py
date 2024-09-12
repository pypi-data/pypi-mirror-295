from typing import Final


REGISTER_AGENT_PATH: Final[str] = '/agent/register'
UNREGISTER_AGENT_PATH: Final[str] = '/agent/<agent_id>'
SUBMIT_OPERATION_PATH: Final[str] = '/agent/<agent_id>/operation/submit'
UPDATE_OPERATION_RESULT_PATH: Final[str] = '/agent/<agent_id>/operation/<operation_id>/result'
SYSTEM_UPDATE_PATH: Final[str] = '/agent/<agent_id>/system_update'

REGISTER_AGENT_FORMAT: Final[str] = REGISTER_AGENT_PATH
UNREGISTER_AGENT_FORMAT: Final[str] = UNREGISTER_AGENT_PATH.replace('<agent_id>', '{agent_id}')
SUBMIT_OPERATION_FORMAT: Final[str] = SUBMIT_OPERATION_PATH.replace('<agent_id>', '{agent_id}')
UPDATE_OPERATION_RESULT_FORMAT: Final[str] = UPDATE_OPERATION_RESULT_PATH.replace('<agent_id>', '{agent_id}').replace('<operation_id>', '{operation_id}')
SYSTEM_UPDATE_FORMAT: Final[str] = SYSTEM_UPDATE_PATH.replace('<agent_id>', '{agent_id}')
