from typing import List, Union

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class FailedTaskResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.FAILURE, message)


class DivideTaskResponse(PromptResponse):
    def __init__(self, reason: str):
        super().__init__(PromptStatus.POSTPONED, reason)

    def reason(self) -> str:
        return self.message


def divide_task_callback(task: Task, reason: str) -> DivideTaskResponse:
    return DivideTaskResponse(reason)


class ExecuteTaskResponse(PromptResponse):
    def __init__(self, task: Task, reason: str):
        super().__init__(PromptStatus.OK, reason, {"task": task})

    def reason(self) -> str:
        return self.message

    def task(self) -> Task:
        return self.data["task"]


def execute_task_callback(
    task: Task, task_id: str, reason: str = ""
) -> Union[ExecuteTaskResponse, FailedTaskResponse]:
    try:
        target_task = task.index[task_id]
        return ExecuteTaskResponse(target_task, reason)
    except IndexError:
        return FailedTaskResponse(f"Task with id {task_id} not found")


class AddTaskDependenciesResponse(PromptResponse):
    def __init__(self, tasks: List[Task]):
        super().__init__(PromptStatus.OK, "", {"tasks": tasks})

    def tasks(self) -> List[Task]:
        return self.data["tasks"]


def add_task_depedencies_callback(
    task: Task, tasks_ids: str
) -> Union[AddTaskDependenciesResponse, FailedTaskResponse]:
    # TODO: Add id safe check
    ids = tasks_ids.split(",")
    tasks = task.get_tasks_by_ids(ids)
    if tasks:
        return AddTaskDependenciesResponse(tasks)
    return FailedTaskResponse(f"Tasks with ids {tasks_ids} not found")
