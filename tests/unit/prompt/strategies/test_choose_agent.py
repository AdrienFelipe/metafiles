from agent.agent_proxy import AgentProxy
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.callbacks.choose_agent import ChooseAgentResponse, FailedChooseAgentResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task.task import Task


def test_choose_agent_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.choose_agent(task)
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)


def test_choose_agent_agent_proxy_success():
    agent_roles = ["role 1", "role 2"]
    arguments = {"roles": ", ".join(agent_roles)}
    agent = FakeAgent([PromptCallbackResponse("ask_agents", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_for_agent_roles(task)
    assert isinstance(response, ChooseAgentResponse)
    assert response.is_successful(), "Response should be successful"
    assert response.get_roles() == agent_roles, "Incorect roles"


def test_choose_agent_agent_proxy_invalid_callback():
    agent_roles = ["role 1", "role 2"]
    arguments = {"roles": ", ".join(agent_roles)}
    agent = FakeAgent([PromptCallbackResponse("invalid_callback", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_for_agent_roles(task)
    assert isinstance(response, FailedChooseAgentResponse)
    assert not response.is_successful(), "Response should not be successful"
    assert response.get_roles() == [], "Incorect roles"
    assert response.get_message(), "Expected non-empty message"


def test_choose_agent_agent_proxy_invalid_arguments():
    arguments = {"invalid_key": "value"}
    agent = FakeAgent([PromptCallbackResponse("ask_agents", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_for_agent_roles(task)
    assert isinstance(response, FailedChooseAgentResponse)
    assert not response.is_successful(), "Response should not be successful"
    assert response.get_roles() == [], "Incorect roles"
    assert response.get_message(), "Expected non-empty message"
