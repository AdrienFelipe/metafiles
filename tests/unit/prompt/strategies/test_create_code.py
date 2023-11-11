from unittest.mock import patch

from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_callback_response_helper import PromptCallbackResponseHelper
from helpers.prompt_helper import (
    assert_prompt_callbacks_are_valid,
    get_callback_response,
    prompt_function_to_callback_arguments,
)
from prompt.callbacks.choose_action import ChooseActionResponse
from prompt.callbacks.choose_agent import ChooseAgentResponse
from prompt.callbacks.code import CreateCodeResponse, NoCodeResponse
from prompt.callbacks.plan import CreatePlanResponse
from prompt.commands.create_code_command import CreateCodeCommand
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse
from prompt.strategies.choose_action import ChooseActionStrategy
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_plan import CreatePlanStrategy
from prompt.strategies.filter_requirements import FilterRequirementsStrategy
from task.task import Task


def test_create_code_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.create_code(task, "reason")

    specials = {
        "code": "print('ok')",
        "tasks_ids": f"{task.id},{task.id}",
        "task_id": task.id,
    }
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt, specials)


def test_create_code_agent_proxy_success():
    root_task = Task("root")
    sub_task1 = Task("sub task 1", parent=root_task)
    sub_task2 = Task("sub task 2", parent=root_task)

    task = Task("test", "test", parent=sub_task2)
    prompt = PromptFactory.create_code(task, "reason")

    sub_task1.action = ActionName.NO_ACTION

    sub_task1.result = ActionResult(ActionResultStatus.SUCCESS, "sub task 1 result")
    sub_task2.result = ActionResult(ActionResultStatus.SUCCESS, "sub task 2 result")

    callback_helper = PromptCallbackResponseHelper().with_code().with_plan()
    callback_helper.arguments = {
        **callback_helper.arguments,
        **{"task_id": sub_task1.id, "tasks_ids": "0,1", "reason": "Test reason!"},
    }
    execute_code_response = get_callback_response(prompt, "execute_code", callback_helper.arguments)

    agent = FakeAgent(keep_last=True)
    agent.add_strategy_responses(
        {
            ChooseAgentStrategy: [ChooseAgentResponse(["Tester role"])],
            CreatePlanStrategy: [CreatePlanResponse(callback_helper.get_plan())],
            FilterRequirementsStrategy: [PromptMessageResponse("This is a test!")],
            ChooseActionStrategy: [ChooseActionResponse(ActionName.RUN_CODE, "Run code")],
        }
    )

    for function in prompt.functions():
        function_name = function["name"]
        callback = function_name
        assert isinstance(callback, str), "function name should be a string"
        responses = [
            PromptCallbackResponse(
                function_name,
                prompt_function_to_callback_arguments(function, callback_helper.arguments),
            ),
            # Always end by a code execution
            execute_code_response,
        ]
        agent.add_responses(responses, reset=True)

        try:
            with patch("builtins.input", return_value="This is a test!"):
                result = CreateCodeCommand.ask(agent, task)
        except Exception as e:
            assert False, f"{function_name} should not raise an exception: {e}"

        if function_name == "divide_task":
            assert isinstance(result, NoCodeResponse)
            assert (
                result.is_successful() != ActionResultStatus.SUCCESS
            ), f"{function_name}: Response should not be successful - {result.message}"
            assert (
                result.reason() == "Test reason!"
            ), f"{function_name}: Invalid message - {result.message}"
        else:
            assert isinstance(result, CreateCodeResponse)
            assert (
                result.is_successful()
            ), f"{function_name}: Response should be successful - {result.message}"
            assert callback_helper.get_code() == result.get_code(), f"{function_name}: Invalid code - {result.message}"
