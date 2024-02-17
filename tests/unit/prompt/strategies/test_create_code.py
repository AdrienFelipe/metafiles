from unittest.mock import patch

from action.action_name import ActionName
from agent.agents.fake_agent import FakeAgent
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from helpers.prompt_callback_response_helper import PromptCallbackResponseHelper
from helpers.prompt_helper import (
    assert_prompt_callbacks_are_valid,
    get_callback_response,
    prompt_function_to_callback_arguments,
)
from prompt.callbacks.choose_agent import ChooseAgentResponse
from prompt.callbacks.code import CreateCodeResponse
from prompt.callbacks.review_result import ReviewResultResponse
from prompt.commands.create_code_command import CreateCodeCommand
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse, PromptStatus
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_code import CreateCodeStrategy
from prompt.strategies.review_result import ReviewResultStrategy
from task.task import Task


def test_create_code_callbacks(logger: IExecutionLogger):
    parent_task = Task("Parent task", "Parent task definition")
    Task("Previous task 1", "Previous task 1 definition", parent=parent_task)
    Task("Previous task 2", "Previous task 2 definition", parent=parent_task)
    task = Task("Task goal", "Task definition", parent=parent_task)
    prompt = PromptFactory.create_code(task)

    specials = {
        "code": "print('ok')",
        "tasks_ids": "0.0, 0.1",
        "task_id": "0.1",
    }
    assert_prompt_callbacks_are_valid(FakeAgent(logger), prompt, specials)


def test_create_code_command_responses(container: ServiceContainer, logger: IExecutionLogger):
    prompt = PromptFactory.create_code(Task("dummy"))

    for function in prompt.functions():
        function_name = str(function["name"])

        # Use a multi-level task
        parent_task = Task("Parent task", "Parent task definition")
        Task("Previous task 1", "Previous task 1 definition", parent=parent_task)
        Task("Previous task 2", "Previous task 2 definition", parent=parent_task)
        task = Task("Task goal", "Task definition", parent=parent_task)

        agent = FakeAgent(logger, keep_last=True)
        callback_helper = PromptCallbackResponseHelper().with_code()
        # Add a default wildcard response
        agent.add_responses([PromptMessageResponse("Default response")])
        should_have_code = setup_command_responses(function_name, agent, task, callback_helper)

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
                result = CreateCodeCommand(container, agent, task).ask()
        except Exception as e:
            assert False, f"{function_name} should not raise an exception: {e}"

        assert isinstance(result, CreateCodeResponse)
        assert (
            not result.is_failure()
        ), f"{function_name}: Response should not fail - {result.message}"

        if should_have_code:
            assert (
                result.code() == callback_helper.get_code()
            ), f"{function_name}: Invalid code - {result.message}"
        else:
            assert result.code() == "", f"{function_name}: Invalid code - {result.message}"


def setup_command_responses(
    function_name: str, agent: FakeAgent, task: Task, callback_helper: PromptCallbackResponseHelper
) -> bool:
    agent.add_strategy_responses(
        {
            ChooseAgentStrategy: [ChooseAgentResponse(["Tester role"])],
            ReviewResultStrategy: [ReviewResultResponse(PromptStatus.OK)],
        }
    )

    if function_name == "tasks_results":
        callback_helper.arguments["tasks_ids"] = "0,1"

    elif function_name == "execute_task":
        task_index = 1
        task.get_siblings_by_position()[task_index].action = ActionName.NO_ACTION
        callback_helper.arguments["task_id"] = f"{task_index}"

    elif function_name == "validate_code":
        task.code = callback_helper.get_code()

    elif function_name == "divide_task":
        return False

    return True


def test_create_code_with_prompt_message_response(
    container: ServiceContainer, logger: IExecutionLogger
):
    task = Task("Task goal", "Task definition")
    prompt = PromptFactory.create_code(task)
    agent = FakeAgent(logger, keep_last=True)

    callback_helper = PromptCallbackResponseHelper().with_code()
    agent.add_responses(
        [
            PromptMessageResponse("Default response"),
            get_callback_response(prompt, "execute_code", callback_helper.arguments),
        ]
    )

    response = CreateCodeCommand(container, agent, task).ask()
    assert not response.is_failure(), f"Response should not fail - {response.message}"
    assert response.code() == callback_helper.get_code(), f"Invalid code - {response.message}"
