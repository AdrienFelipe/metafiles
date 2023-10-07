from abc import ABC, abstractmethod
from action_result import ActionResult
from openai_chat import OpenAIChat
from task import Task


class Action(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.agent = OpenAIChat()

    @abstractmethod
    def execute(self, task: Task, reason: str) -> ActionResult:
        """Execute the action given a task and a reason."""
        pass
