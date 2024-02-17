from agent.agents.openai_agent import OpenAIAgent
from core.logger.logger_interface import IExecutionLogger
from task.task import Task
from task.task_handler_interface import ITaskHandler


def test_task_execute_create_find_file(task_handler: ITaskHandler, logger: IExecutionLogger):
    task = Task(
        "Find a file named 'hello_world.txt'",
        """You MUST do the following in multiple tasks:
        1. Create a file named 'hello_world.txt'
        2. Write the text 'Hello, World!' in the file
        3. List all files in the current directory
        4. Confirm that the file 'hello_world.txt' exists
        """,
    )
    task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
