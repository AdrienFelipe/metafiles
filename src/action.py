from abc import ABC, abstractmethod
from action_result import ActionResult
from task import Task

class Action(ABC):
    @abstractmethod
    def apply(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""
        pass