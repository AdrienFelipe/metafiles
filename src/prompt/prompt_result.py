from enum import Enum, auto
from typing import Optional, TypeVar


class PromptStatus(Enum):
    COMPLETED = auto()
    FAILURE = auto()
    PENDING = auto()
    POSTPONED = auto()


class PromptResponse:
    def __init__(self, status: PromptStatus, message: str = "", data: Optional[dict] = None):
        self.status = status
        self.message = message.strip()
        self.data = data or {}

    def get_message(self) -> str:
        return self.message

    def is_completed(self) -> bool:
        return self.status == PromptStatus.COMPLETED

    def is_failure(self) -> bool:
        return self.status == PromptStatus.FAILURE

    def __str__(self) -> str:
        return f"Status: {self.status.name}, Message: {self.message}, Data: {self.data}"

    def to_dict(self) -> dict:
        return {"status": self.status.name, "message": self.message, "data": self.data}


class PromptMessageResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.COMPLETED, message)


class PromptCallbackResponse(PromptResponse):
    def __init__(self, function_name: str, function_arguments: dict):
        super().__init__(PromptStatus.COMPLETED, function_name, function_arguments)

    def callback_name(self) -> str:
        return self.message

    def callback_arguments(self) -> dict:
        return self.data


class PostponeResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.POSTPONED, message)


class FailedPromptResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.FAILURE, message)


TPromptResponse = TypeVar("TPromptResponse", bound=PromptResponse)
