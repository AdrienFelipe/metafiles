from agent.agents.openai_agent import OpenAIAgent
from core.logger.test_logger import TestLogger
from task.task import Task
from task.task_handler import TaskHandler


def test_task_direct_dependency():
    logger = TestLogger(name_suffix="test_task_direct_dependency")

    result_1 = 32
    result_2 = result_1 * 2
    result_3 = "final"
    expected_result = f"1: {result_1}, 2: {result_2}, 3: {result_3}"

    parent_task = Task("Concatenate strings", "Obtain 3 different results and concatenate them as '1: [result 1], 2: [result 2], 3: [result 3]'") 
    Task("Obtain result 1", f"This task should return the number '{result_1}'", parent=parent_task)
    Task("Obtain result 2", "Double the number returned by previous task and return it", parent=parent_task)

    task = Task(
        "Return concatenated results",
        f"""
        Result 3 is '{result_3}'
        Read results from previous tasks and concatenate the results as:
        '1: [task 1 value], 2: [task 2 value], 3: [result 3]'
        """,
        parent=parent_task,
    )

    Task("A following task that should not appear as available for dependency", parent=parent_task)

    TaskHandler(logger).execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == expected_result, "Incorrect result"
