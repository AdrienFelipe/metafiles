from abc import ABC, abstractmethod

from action_result import ActionResult
from task import Task


class Action(ABC):
    @abstractmethod
    def execute(self, task: Task, agent_proxy, reason: str) -> ActionResult:
        """Execute the action given a task and a reason."""
