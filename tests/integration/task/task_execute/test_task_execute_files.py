from agent.agents.openai_agent import OpenAIAgent
from core.logger.test_logger import TestLogger
from task.task import Task
from task.task_execute import TaskHandler


def test_task_execute_create_find_file():
    task = Task(
        "Find a file named 'hello_world.txt'",
        """You MUST do the following in multiple tasks:
        1. Create a file named 'hello_world.txt'
        2. Write the text 'Hello, World!' in the file
        3. List all files in the current directory
        4. Confirm that the file 'hello_world.txt' exists
        """,
    )
    logger = TestLogger(name_suffix="test_task_execute_create_find_file")
    TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
