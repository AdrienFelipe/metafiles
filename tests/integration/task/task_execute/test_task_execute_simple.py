from unittest.mock import patch

from agent.agents.openai_agent import OpenAIAgent
from core.logger.logger_interface import IExecutionLogger
from task.task import Task
from task.task_handler_interface import ITaskHandler


def test_task_execute_print_hello(task_handler: ITaskHandler, logger: IExecutionLogger):
    task = Task(
        "Run code to print the exact string 'Hello, World!'",
        "This is a test task, just run the code",
    )
    task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Hello, World!", "Incorrect result"


def test_task_execute_ask_user_print_string(task_handler: ITaskHandler, logger: IExecutionLogger):
    task = Task(
        "Ask the user for a string and print it as is using code",
        "You don't need details about the task, just create the code that is asked",
    )

    with patch("builtins.input", return_value="Hello, World User!"):
        task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Hello, World User!", "Incorrect result"


def test_task_execute_ask_two_steps_code(task_handler: ITaskHandler, logger: IExecutionLogger):
    task = Task(
        "Create a custom_print function that prints 'Custom: {text argument}'",
        """
        Create the function and then run it with the argument 'Hello, World!'
        Divide into two separate tasks, the final output being the result of the execution.
        """,
    )

    with patch("builtins.input", return_value="Just follow the instructions!"):
        task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Custom: Hello, World!", "Incorrect result"


def test_task_execute_search_wikipedia(task_handler: ITaskHandler, logger: IExecutionLogger):
    task = Task(
        "Search wikipedia for 'Hello, World!'",
        """
        Print the first search result for 'Hello, World!'
        """,
    )

    with patch("builtins.input", return_value="Use the simplest free option"):
        task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == '"Hello, World!" program', "Incorrect result"
