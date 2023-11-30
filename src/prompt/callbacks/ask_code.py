from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class AskForCodeResponse(PromptResponse):
    def __init__(
        self,
        reason: str,
        status: PromptStatus = PromptStatus.COMPLETED,
    ):
        super().__init__(status, reason)

    def reason(self) -> str:
        return self.message


def ask_for_code_callback(task: Task, reason: str = "", **kwargs) -> AskForCodeResponse:
    return AskForCodeResponse(reason)
