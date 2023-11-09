from unittest.mock import patch

from agent.agent_proxy import AgentProxy
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_callback_response_helper import PromptCallbackResponseHelper
from helpers.prompt_helper import (
    assert_prompt_callbacks_are_valid,
    get_callback_response,
    prompt_function_to_callback_arguments,
)
from prompt.callbacks.plan import CreatePlanResponse, FailedCreatePlanResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse
from task.task import Task


def test_create_plan_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.create_plan(task, "role")
    arguments = PromptCallbackResponseHelper.simple()
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt, arguments)


def test_create_plan_callbacks_with_plan():
    callback_helper = PromptCallbackResponseHelper().with_plan()
    task = Task("test", "test")
    task.plan = callback_helper.get_plan()

    prompt = PromptFactory.create_plan(task, "role")
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt, callback_helper.arguments)


def test_create_plan_agent_proxy_success():
    callback_helper = PromptCallbackResponseHelper().with_plan()
    plan = callback_helper.get_plan()

    agent = FakeAgent([PromptCallbackResponse("update_plan", callback_helper.arguments)])
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
    callback_helper = PromptCallbackResponseHelper().with_plan()
    plan = callback_helper.get_plan()
    responses = [
        PromptCallbackResponse("ask_user", {"query": "some question"}),
        PromptMessageResponse("some answer"),
        PromptCallbackResponse("update_plan", callback_helper.arguments),
    ]
    agent = FakeAgent(responses)
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    with patch("builtins.input", return_value="user response"):
        response = agent_proxy.ask_to_create_plan(task, "some role")

    assert isinstance(response, CreatePlanResponse)
    assert response.is_successful(), "Response should be successful"
    assert response.get_plan() == plan, "Incorrect plan"


def test_create_plan_agent_proxy_responses_are_valid():
    agent = FakeAgent()
    agent_proxy, task = AgentProxy(agent), Task("test", "test")
    prompt = PromptFactory.create_plan(task, "role")
    specials = PromptCallbackResponseHelper.simple()
    callback_response = get_callback_response(prompt, "update_plan", specials)

    for function in prompt.functions():
        callback = function["name"]
        assert isinstance(callback, str), "function name should be a string"
        responses = [
            PromptCallbackResponse(
                function["name"], prompt_function_to_callback_arguments(function, specials)
            ),
            # Always end by a code execution
            callback_response,
        ]
        agent.add_responses(responses, reset=True)

        with patch("builtins.input", return_value="This is a test!"):
            response = agent_proxy.ask_to_create_plan(task, prompt.strategy.agent_role)

        assert isinstance(response, CreatePlanResponse)
        assert response.is_successful(), f"Response should be successful: {response.message}"
