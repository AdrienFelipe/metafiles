from typing import List, Union

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class FailedTaskResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.FAILURE, message)


class DivideTaskResponse(PromptResponse):
    def __init__(self, reason: str):
        super().__init__(PromptStatus.SUCCESS, reason)

    def reason(self) -> str:
        return self.message


def divide_task_callback(task: Task, reason: str) -> DivideTaskResponse:
    return DivideTaskResponse(reason)


class ExecuteTaskResponse(PromptResponse):
    def __init__(self, task: Task, reason: str):
        super().__init__(PromptStatus.SUCCESS, reason, {"task": task})

    def reason(self) -> str:
        return self.message

    def task(self) -> Task:
        return self.data["task"]


def execute_task_callback(
    task: Task, task_id: str, reason: str
) -> Union[ExecuteTaskResponse, FailedTaskResponse]:
    try:
        target_task = task.get_siblings()[int(task_id)]
        return ExecuteTaskResponse(target_task, reason)
    except IndexError:
        return FailedTaskResponse(f"Task with id {task_id} not found")


class GetTasksResultsResponse(PromptResponse):
    def __init__(self, tasks: List[Task]):
        super().__init__(PromptStatus.SUCCESS, "", {"tasks": tasks})

    def tasks(self) -> List[Task]:
        return self.data["tasks"]


def get_tasks_results_callback(
    task: Task, tasks_ids: str
) -> Union[GetTasksResultsResponse, FailedTaskResponse]:
    # TODO: Add id safe check
    tasks_ids_list = [int(task_id) for task_id in tasks_ids.split(",")]
    tasks = task.get_siblings(tasks_ids_list)
    if tasks:
        return GetTasksResultsResponse(tasks)
    return FailedTaskResponse(f"Tasks with ids {tasks_ids} not found")
