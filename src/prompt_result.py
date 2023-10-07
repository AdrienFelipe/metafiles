from enum import Enum, auto


class PromptStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    PENDING = auto()


class PromptResponse:
    def __init__(self, status: PromptStatus, message: str = "", data: dict = None):
        self.status = status
        self.message = message
        self.data = data or {}

    def is_successful(self) -> bool:
        return self.status == PromptStatus.SUCCESS

    def __str__(self) -> str:
        return f"Status: {self.status.name}, Message: {self.message}, Data: {self.data}"

    def to_dict(self) -> dict:
        return {"status": self.status.name, "message": self.message, "data": self.data}


class PromptMessageResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.SUCCESS, message, None)
