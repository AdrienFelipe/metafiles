from unittest.mock import patch

from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import (
    assert_prompt_callbacks_are_valid,
    prompt_function_to_callback_arguments,
)
from prompt.callbacks.choose_action import ChooseActionResponse
from prompt.callbacks.choose_agent import ChooseAgentResponse
from prompt.callbacks.code import CreateCodeResponse
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
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)


def test_create_code_agent_proxy_success():
    code = "var = 'ok'\nprint(var)"
    arguments = {"code": code, "test_args": "{}", "tasks_ids": "", "update_reason": ""}

    root_task = Task("root")
    sub_task1 = Task("sub task 1", parent=root_task)
    sub_task2 = Task("sub task 2", parent=root_task)
    task = Task("test", "test", parent=sub_task2)

    sub_task1.action = ActionName.NO_ACTION

    sub_task1.result = ActionResult(ActionResultStatus.SUCCESS, "sub task 1 result")
    sub_task2.result = ActionResult(ActionResultStatus.SUCCESS, "sub task 2 result")

    specials = {
        "task_id": sub_task1.id,
        "tasks_ids": f"{sub_task1.id}, {sub_task2.id}",
        "update_reason": "some reason",
        "code": code,
    }

    agent = FakeAgent(keep_last=True)
    prompt = PromptFactory.create_code(task, "reason")

    for function in prompt.functions():
        function_name = function["name"]
        callback = function_name
        assert isinstance(callback, str), "function name should be a string"
        responses = [
            PromptCallbackResponse(
                function_name, prompt_function_to_callback_arguments(function, specials)
            ),
            # Always end by a code execution
            PromptCallbackResponse("execute_code", arguments),
        ]
        agent.add_responses(responses)
        agent.add_strategy_responses(
            {
                ChooseAgentStrategy: [ChooseAgentResponse(["Tester role"])],
                CreatePlanStrategy: [CreatePlanResponse(["Step 1", "Step 2"])],
                FilterRequirementsStrategy: [PromptMessageResponse("This is a test!")],
                ChooseActionStrategy: [ChooseActionResponse(ActionName.RUN_CODE, "Run code")],
            }
        )

        try:
            with patch("builtins.input", return_value="This is a test!"):
                result = CreateCodeCommand.ask(agent, task)
        except Exception as e:
            assert False, f"{function_name} should not raise an exception: {e}"

        assert isinstance(result, CreateCodeResponse)
        assert result.is_successful(), f"{function_name}: Response should be successful"
        assert result.get_code() == code, f"{function_name}: Incorrect code"
