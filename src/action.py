from abc import ABC, abstractmethod

from action_result import ActionResult
from task import Task


class Action(ABC):
    @abstractmethod
    def execute(self, task: Task, reason: str = "") -> ActionResult:
        """Execute the action given a task and a reason."""
