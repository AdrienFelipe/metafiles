from enum import Enum, auto


class ActionResultStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    PENDING = auto()


class ActionResult:
    def __init__(self, status: ActionResultStatus, message: str = "", data: dict = None):
        """
        Initialize an ActionResult instance.

        :param status: The result's status.
        :param message: Optional message regarding the action.
        :param data: Optional dictionary containing additional data about the action's outcome.
        """
        self.status = status
        self.message = message
        self.data = data or {}

    def is_successful(self) -> bool:
        """Return True if the action was successful."""
        return self.status == ActionResultStatus.SUCCESS

    def __str__(self) -> str:
        return f"Status: {self.status.name}, Message: {self.message}, Data: {self.data}"

    def to_dict(self) -> dict:
        """Convert the result into a dictionary format."""
        return {"status": self.status.name, "message": self.message, "data": self.data}
