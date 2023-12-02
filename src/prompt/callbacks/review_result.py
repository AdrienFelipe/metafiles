from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class ReviewResultResponse(PromptResponse):
    def __init__(self, status: PromptStatus, reason: str = ""):
        super().__init__(status, message=reason)

    def reason(self) -> str:
        return self.message


class FailedReviewResultResponse(ReviewResultResponse):
    def __init__(self, reason: str):
        super().__init__(PromptStatus.FAILURE, reason)


def approve_result_callback(task: Task, **kwargs) -> ReviewResultResponse:
    return ReviewResultResponse(PromptStatus.OK)


def reject_result_callback(task: Task, reason: str, **kwargs) -> ReviewResultResponse:
    return ReviewResultResponse(PromptStatus.POSTPONED, reason)
