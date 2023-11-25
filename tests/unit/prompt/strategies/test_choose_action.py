from action.action_name import ActionName
from agent.agent_proxy import AgentProxy
from agent.agents.fake_agent import FakeAgent
from core.logger.no_logger import NoLogger
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.callbacks.choose_action import ChooseActionResponse, FailedChooseActionResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task.task import Task


def test_choose_action_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.choose_action(task)
    assert_prompt_callbacks_are_valid(FakeAgent(NoLogger()), prompt)


def test_choose_action_agent_proxy_success():
    action, reason = ActionName.RUN_CODE, "test code"
    arguments = {"action_key": action.value, "reason": reason}
    agent = FakeAgent(NoLogger(), [PromptCallbackResponse("apply_action", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_choose_action(task)
    assert isinstance(response, ChooseActionResponse)
    assert response.is_completed(), "Response should be successful"
    assert response.action_name() == action, "Action is not correct"
    assert response.reason() == reason, "Reason is not correct"


def test_choose_action_agent_proxy_invalid_callback():
    action, reason = ActionName.RUN_CODE, "test code"
    arguments = {"action_key": action.value, "reason": reason}
    agent = FakeAgent(NoLogger(), [PromptCallbackResponse("invalid_callback", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_choose_action(task)
    assert isinstance(response, FailedChooseActionResponse)
    assert not response.is_completed(), "Response should not be successful"
    assert response.action_name() == ActionName.NO_ACTION, "Action is not correct"
    assert response.reason(), "Expected non-empty reason"


def test_choose_action_agent_proxy_invalid_action():
    action, reason = "invalid_action", "test code"
    arguments = {"action_key": action, "reason": reason}
    agent = FakeAgent(NoLogger(), [PromptCallbackResponse("apply_action", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_choose_action(task)
    assert isinstance(response, FailedChooseActionResponse)
    assert not response.is_completed(), "Response should not be successful"
    assert response.action_name() == ActionName.NO_ACTION, "Action is not correct"
    assert response.reason(), "Expected non-empty reason"


def test_choose_action_agent_proxy_invalid_arguments():
    arguments = {"invalid_key": "value"}
    agent = FakeAgent(NoLogger(), [PromptCallbackResponse("apply_action", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_choose_action(task)
    assert isinstance(response, FailedChooseActionResponse)
    assert not response.is_completed(), "Response should not be successful"
    assert response.action_name() == ActionName.NO_ACTION, "Action is not correct"
    assert response.reason(), "Expected non-empty reason"
