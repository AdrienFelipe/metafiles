from enum import Enum, auto
from typing import Optional


class PromptStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    PENDING = auto()


class PromptResponse:
    def __init__(self, status: PromptStatus, message: str = "", data: Optional[dict] = None):
        self.status = status
        self.message = message
        self.data = data or {}

    def get_message(self) -> str:
        return self.message

    def is_successful(self) -> bool:
        return self.status == PromptStatus.SUCCESS

    def __str__(self) -> str:
        return f"Status: {self.status.name}, Message: {self.message}, Data: {self.data}"

    def to_dict(self) -> dict:
        return {"status": self.status.name, "message": self.message, "data": self.data}


class PromptMessageResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.SUCCESS, message)


class PromptCallbackResponse(PromptResponse):
    def __init__(self, function_name: str, function_arguments: dict):
        super().__init__(PromptStatus.SUCCESS, function_name, function_arguments)

    def get_function_name(self) -> str:
        return self.message

    def get_function_arguments(self) -> dict:
        return self.data


class FailedPromptResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.FAILURE, message)
