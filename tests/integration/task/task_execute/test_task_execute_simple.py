from unittest.mock import patch

from agent.agents.openai_agent import OpenAIAgent
from task.task import Task
from task.task_execute import execute_task


def test_task_execute_print_hello():
    agent = OpenAIAgent()
    task = Task(
        "Run code to print the exact string 'Hello, World!'",
        "This is a test task, just run the code",
    )
    execute_task(agent, task)

    assert task.result.is_successful(), "Incorrect status"
    assert task.result.message == "Hello, World!", "Incorrect result"


def test_task_execute_ask_user_print_string():
    agent = OpenAIAgent()
    task = Task(
        "Run code to print the exact string you ask the user",
        "You don't need details about the task, just create the code that is asked",
    )

    with patch("builtins.input", return_value="Hello, World User!"):
        execute_task(agent, task)

    assert task.result.is_successful(), "Incorrect status"
    assert task.result.message == "Hello, World User!", "Incorrect result"
