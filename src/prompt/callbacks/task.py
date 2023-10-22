from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class DivideTaskResponse(PromptResponse):
    def __init__(self, reason: str):
        super().__init__(PromptStatus.SUCCESS, reason)

    def get_reason(self) -> str:
        return self.message


def divide_task_callback(task: Task, reason: str) -> DivideTaskResponse:
    return DivideTaskResponse(reason)


class ExecuteTaskResponse(PromptResponse):
    def __init__(self, task_id: str, reason: str):
        super().__init__(PromptStatus.SUCCESS, reason, {"id": task_id})

    def get_reason(self) -> str:
        return self.message

    def get_task_id(self) -> str:
        return self.data[id]


def execute_task_callback(task: Task, task_id: str, reason: str) -> ExecuteTaskResponse:
    return ExecuteTaskResponse(task_id, reason)


class GetTasksResultsResponse(PromptResponse):
    def __init__(self, task_ids: List[str]):
        super().__init__(PromptStatus.SUCCESS, "", {"ids": task_ids})

    def get_task_ids(self) -> str:
        return self.data["ids"]


def get_tasks_results_callback(task: Task, tasks_ids: str) -> GetTasksResultsResponse:
    tasks_ids_list = [task_id.strip() for task_id in tasks_ids.split(",")]
    return GetTasksResultsResponse(tasks_ids_list)
