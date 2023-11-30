from prompt.prompt_result import PromptMessageResponse
from task.task import Task


class ValidateResponse(PromptMessageResponse):
    ...


def validate_response_callback(task: Task, **kwargs) -> ValidateResponse:
    return ValidateResponse(task.response)
