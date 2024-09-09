
def test_agent():
    from cumulonimbus_models.agent import AgentRegisterRequest, UnregisterAgentRequest, AgentRegisterResponse, UnregisterAgentResponse, UnregisterAgentStatus
    assert AgentRegisterRequest(hostname='test')
    assert UnregisterAgentRequest()
    assert AgentRegisterResponse(agent_id='test', agent_key='test', ip_address='test', operations_queue_url='test')
    assert UnregisterAgentResponse(status='SUCCESS')

