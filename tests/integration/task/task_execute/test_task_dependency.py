from agent.agents.openai_agent import OpenAIAgent
from core.logger.logger_interface import IExecutionLogger
from task.task import Task
from task.task_handler_interface import ITaskHandler


def test_task_direct_dependency(task_handler: ITaskHandler, logger: IExecutionLogger):
    result_1 = 32
    result_2 = result_1 * 2
    result_3 = "final"
    expected_result = f"1: {result_1}, 2: {result_2}, 3: {result_3}"

    parent_task = Task(
        "Concatenate multiple results",
        "Obtain 3 different results and concatenate them as '1: [result 1], 2: [result 2], 3: [result 3]'",
    )
    Task("Output Value1", f"This task should return the number '{result_1}'", parent=parent_task)
    Task(
        "Output Value2",
        "Double the number returned by previous task and return it",
        parent=parent_task,
    )

    task = Task(
        "Concatenate results 1, 2 and 3",
        f"""
        Value1 and Value2 are the respective outputs from the two previous tasks
        Value 3 is equal to '{result_3}'
        Add corresponding dependencies and show the result as:
        '1: [Value1], 2: [Value2], 3: [Value3]'

        """,
        parent=parent_task,
    )

    Task("A following task that should not appear as available for dependency", parent=parent_task)

    task_handler.execute(OpenAIAgent(logger), task)

    assert task.result.is_completed(), "Incorrect status"
    assert task.result.message == expected_result, "Incorrect result"
