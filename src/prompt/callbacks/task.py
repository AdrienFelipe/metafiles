from typing import Set

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


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


def execute_task_callback(task: Task, task_id: str, reason: str) -> ExecuteTaskResponse:
    # TODO: add id safe check
    target_task = task.index[task_id]
    return ExecuteTaskResponse(target_task, reason)


class GetTasksResultsResponse(PromptResponse):
    def __init__(self, tasks: Set[Task]):
        super().__init__(PromptStatus.SUCCESS, "", {"tasks": tasks})

    def tasks(self) -> Set[Task]:
        return self.data["tasks"]


def get_tasks_results_callback(task: Task, tasks_ids: str) -> GetTasksResultsResponse:
    # TODO: Add id safe check
    tasks_ids_list = set(task_id.strip() for task_id in tasks_ids.split(","))
    tasks = task.get_tasks_by_ids(tasks_ids_list)
    return GetTasksResultsResponse(tasks)
