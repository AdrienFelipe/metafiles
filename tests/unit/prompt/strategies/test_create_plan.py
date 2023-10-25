from unittest.mock import patch

import pytest

from agent.agent_proxy import AgentProxy
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.callbacks.plan import CreatePlanResponse, FailedCreatePlanResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse
from task.task import Task


def test_create_plan_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.create_plan(task, "role")
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)


@pytest.mark.parametrize("callback", ["update_plan", "validate_plan"])
def test_create_plan_agent_proxy_success(callback):
    plan = ["step 1", "step 2"]
    arguments = {"plan": "\n".join(plan)}
    agent = FakeAgent([PromptCallbackResponse(callback, arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_create_plan(task, "role")
    assert isinstance(response, CreatePlanResponse)
    assert response.is_successful(), "Response should be successful"
    assert response.get_plan() == plan, "Incorrect plan"


def test_create_plan_agent_proxy_failure():
    agent = FakeAgent([PromptCallbackResponse("invalid_callback", {})])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_to_create_plan(task, "role")
    assert isinstance(response, FailedCreatePlanResponse)
    assert not response.is_successful(), "Response should not be successful"
    assert response.get_message(), "Expected non-empty message"


def test_create_plan_agent_proxy_scenario():
    plan = ["step 1", "step 2"]
    arguments = {"plan": "\n".join(plan)}
    responses = [
        PromptCallbackResponse("ask_user", {"query": "some question"}),
        PromptMessageResponse("some answer"),
        PromptCallbackResponse("update_plan", arguments),
    ]
    agent = FakeAgent(responses)
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    with patch("builtins.input", return_value="user response"):
        response = agent_proxy.ask_to_create_plan(task, "some role")

    assert isinstance(response, CreatePlanResponse)
    assert response.is_successful(), "Response should be successful"
    assert response.get_plan() == plan, "Incorrect plan"
    assert len(agent.responses) == 0, "Expected no more responses"
