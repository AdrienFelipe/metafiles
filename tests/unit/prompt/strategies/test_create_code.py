from unittest.mock import patch

from action.action_name import ActionName
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_callback_response_helper import PromptCallbackResponseHelper
from helpers.prompt_helper import (
    assert_prompt_callbacks_are_valid,
    get_callback_response,
    prompt_function_to_callback_arguments,
)
from prompt.callbacks.choose_agent import ChooseAgentResponse
from prompt.callbacks.code import CreateCodeResponse
from prompt.commands.create_code_command import CreateCodeCommand
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_code import CreateCodeStrategy
from task.task import Task


def test_create_code_callbacks():
    parent_task = Task("Parent task", "Parent task definition")
    Task("Previous task 1", "Previous task 1 definition", parent=parent_task)
    Task("Previous task 2", "Previous task 2 definition", parent=parent_task)
    task = Task("Task goal", "Task definition", parent=parent_task)
    prompt = PromptFactory.create_code(task, "reason")

    specials = {
        "code": "print('ok')",
        "tasks_ids": "0, 1",
        "task_id": "1",
    }
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt, specials)


def test_create_code_command_responses():
    prompt = PromptFactory.create_code(Task("dummy"))

    for function in prompt.functions():
        function_name = function["name"]

        # Use a multi-level task
        parent_task = Task("Parent task", "Parent task definition")
        Task("Previous task 1", "Previous task 1 definition", parent=parent_task)
        Task("Previous task 2", "Previous task 2 definition", parent=parent_task)
        task = Task("Task goal", "Task definition", parent=parent_task)

        agent = FakeAgent(keep_last=True)
        callback_helper = PromptCallbackResponseHelper().with_code()
        # Add a default wildcard response
        agent.add_responses([PromptMessageResponse("Default response")])
        expected_success = setup_command_responses(function_name, agent, task, callback_helper)

        agent.add_strategy_responses(
            {
                CreateCodeStrategy: [
                    # Main execution response
                    PromptCallbackResponse(
                        function_name,
                        prompt_function_to_callback_arguments(function, callback_helper.arguments),
                    ),
                    # Always end by a code execution
                    get_callback_response(prompt, "execute_code", callback_helper.arguments),
                ]
            }
        )

        try:
            with patch("builtins.input", return_value="This is a test!"):
                result = CreateCodeCommand.ask(agent, task)
        except Exception as e:
            assert False, f"{function_name} should not raise an exception: {e}"

        assert isinstance(result, CreateCodeResponse)
        assert (
            result.is_successful() == expected_success
        ), f"{function_name}: Response should be successful - {result.message}"

        if expected_success:
            assert (
                result.get_code() == callback_helper.get_code()
            ), f"{function_name}: Invalid code - {result.message}"
        else:
            assert result.get_code() == "", f"{function_name}: Invalid code - {result.message}"


def setup_command_responses(
    function_name: str, agent: FakeAgent, task: Task, callback_helper: PromptCallbackResponseHelper
) -> bool:
    agent.add_strategy_responses({ChooseAgentStrategy: [ChooseAgentResponse(["Tester role"])]})

    if function_name == "tasks_results":
        callback_helper.arguments["tasks_ids"] = "0,1"

    elif function_name == "execute_task":
        task_index = 1
        task.get_siblings()[task_index].action = ActionName.NO_ACTION
        callback_helper.arguments["task_id"] = f"{task_index}"

    elif function_name == "validate_code":
        task.code = callback_helper.get_code()

    elif function_name == "divide_task":
        return False

    return True
