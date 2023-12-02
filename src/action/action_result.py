from enum import Enum, auto


class ActionResultStatus(Enum):
    COMPLETED = auto()
    FAILURE = auto()
    PENDING = auto()

    @property
    def icon(self):
        return {
            ActionResultStatus.COMPLETED: "✅",
            ActionResultStatus.FAILURE: "❌",
            ActionResultStatus.PENDING: "🚧",
        }[self]


class ActionResult:
    def __init__(self, status: ActionResultStatus, message: str = "", data: dict = {}):
        """
        Initialize an ActionResult instance.

        :param status: The result's status.
        :param message: Optional message regarding the action.
        :param data: Optional dictionary containing additional data about the action's outcome.
        """
        self.status = status
        self.message = message
        self.data = data or {}

    def is_completed(self) -> bool:
        """Return True if the action was successful."""
        return self.status == ActionResultStatus.COMPLETED

    def __str__(self) -> str:
        return f"Status: {self.status.name}, Message: {self.message}, Data: {self.data}"

    def to_dict(self) -> dict:
        """Convert the result into a dictionary format."""
        return {"status": self.status.name, "message": self.message, "data": self.data}
