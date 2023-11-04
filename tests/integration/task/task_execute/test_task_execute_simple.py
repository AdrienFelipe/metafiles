from unittest.mock import patch

from agent.agents.openai_agent import OpenAIAgent
from task.task import Task
from task.task_execute import execute_task


def test_task_execute_print_hello():
    task = Task(
        "Run code to print the exact string 'Hello, World!'",
        "This is a test task, just run the code",
    )
    execute_task(OpenAIAgent(), task)

    assert task.result.is_successful(), "Incorrect status"
    assert task.result.message == "Hello, World!", "Incorrect result"


def test_task_execute_ask_user_print_string():
    task = Task(
        "Run code to print the exact string you ask the user",
        "You don't need details about the task, just create the code that is asked",
    )

    with patch("builtins.input", return_value="Hello, World User!"):
        execute_task(OpenAIAgent(), task)

    assert task.result.is_successful(), "Incorrect status"
    assert task.result.message == "Hello, World User!", "Incorrect result"


def test_task_execute_ask_two_steps_code():
    task = Task(
        "Create a custom_print function that prints 'Custom: {text argument}'",
        """
        Create the function and then run it with the argument 'Hello, World!'
        Divide into two separate tasks, the final output being the result of the execution.
        """,
    )

    with patch("builtins.input", return_value="Just follow the instructions!"):
        execute_task(OpenAIAgent(), task)

    assert task.result.is_successful(), "Incorrect status"
    assert task.result.message == "Custom: Hello, World!", "Incorrect result"
