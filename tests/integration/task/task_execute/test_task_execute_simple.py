from unittest.mock import patch

from agent.agents.openai_agent import OpenAIAgent
from core.logger.test_logger import TestLogger
from task.task import Task
from task.task_execute import TaskHandler


def test_task_execute_print_hello():
    task = Task(
        "Run code to print the exact string 'Hello, World!'",
        "This is a test task, just run the code",
    )
    logger = TestLogger(name_suffix="test_task_execute_print_hello")
    TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Hello, World!", "Incorrect result"


def test_task_execute_ask_user_print_string():
    task = Task(
        "Ask the user for a string and print it using code",
        "You don't need details about the task, just create the code that is asked",
    )
    logger = TestLogger(name_suffix="test_task_execute_ask_user_print_string")

    with patch("builtins.input", return_value="Hello, World User!"):
        TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Hello, World User!", "Incorrect result"


def test_task_execute_ask_two_steps_code():
    task = Task(
        "Create a custom_print function that prints 'Custom: {text argument}'",
        """
        Create the function and then run it with the argument 'Hello, World!'
        Divide into two separate tasks, the final output being the result of the execution.
        """,
    )
    logger = TestLogger(name_suffix="test_task_execute_ask_two_steps_code")

    with patch("builtins.input", return_value="Just follow the instructions!"):
        TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == "Custom: Hello, World!", "Incorrect result"


def test_task_execute_search_wikipedia():
    task = Task(
        "Search wikipedia for 'Hello, World!'",
        """
        Print the first search result for 'Hello, World!'
        """,
    )
    logger = TestLogger(name_suffix="test_task_execute_search_wikipedia")

    with patch("builtins.input", return_value="Use the simplest free option"):
        TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == '"Hello, World!" program', "Incorrect result"
