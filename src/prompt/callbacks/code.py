import json
from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class CreateCodeResponse(PromptResponse):
    def __init__(
        self,
        code: str,
        test_args: dict,
        tasks_ids: List[str],
        update_reason: str,
        status: PromptStatus = PromptStatus.SUCCESS,
    ):
        data = {"test_args": test_args, "tasks_ids": tasks_ids, "update_reason": update_reason}
        super().__init__(status, code, data)

    def get_code(self) -> str:
        return self.message

    def get_test_args(self) -> dict:
        return self.data["test_args"]

    def get_tasks_ids(self) -> List[str]:
        return self.data["tasks_ids"]

    def get_update_reason(self) -> str:
        return self.data["update_reason"]


def create_code_callback(
    task: Task, code: str, test_args: str, tasks_ids: str, update_reason: str
) -> CreateCodeResponse:
    test_args_dict = json.loads(test_args)
    tasks_ids_list = [task_id.strip() for task_id in tasks_ids.split(",")]
    return CreateCodeResponse(code, test_args_dict, tasks_ids_list, update_reason)


class ValidateCodeResponse(PromptResponse):
    def __init__(self, code: str):
        super().__init__(PromptStatus.SUCCESS, code)

    def get_code(self) -> str:
        return self.message


def validate_code_callback(task: Task) -> ValidateCodeResponse:
    return ValidateCodeResponse("\n\n".join(task.plan))


class FailedCreateCodeResponse(CreateCodeResponse):
    def __init__(self, message: str):
        super().__init__(message, {}, [], "", PromptStatus.FAILURE)
