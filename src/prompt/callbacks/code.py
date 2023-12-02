from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class CreateCodeResponse(PromptResponse):
    def __init__(
        self,
        code: str,
        change_log: str,
        tasks_ids: List[str],
        status: PromptStatus = PromptStatus.PENDING,
    ):
        data = {"tasks_ids": tasks_ids, "change_log": change_log}
        super().__init__(status, code, data)

    def code(self) -> str:
        return self.message

    def tasks_ids(self) -> List[str]:
        return self.data["tasks_ids"]

    def change_log(self) -> str:
        return self.data["change_log"]


def create_code_callback(
    task: Task, code: str, change_log: str, tasks_ids: str = "", **kwargs
) -> CreateCodeResponse:
    ids = [task_id.strip() for task_id in tasks_ids.split(",")]
    return CreateCodeResponse(code, change_log, ids)


class ValidateCodeResponse(CreateCodeResponse):
    def __init__(self, code: str):
        super().__init__(
            code,
            # TODO: not sure this should be hardcoded here as empty
            change_log="",
            tasks_ids=[],
            status=PromptStatus.OK,
        )

    def code(self) -> str:
        return self.message


def validate_code_callback(task: Task, **kwargs) -> ValidateCodeResponse:
    return ValidateCodeResponse(task.code)


class FailedCreateCodeResponse(CreateCodeResponse):
    def __init__(self, message: str):
        super().__init__(message, "", [], PromptStatus.FAILURE)


class NoCodeResponse(CreateCodeResponse):
    def __init__(self, reason: str):
        super().__init__("", reason, [], PromptStatus.POSTPONED)
