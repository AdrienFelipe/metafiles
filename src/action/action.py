from abc import ABC, abstractmethod

from action.action_result import ActionResult
from agent.agent_interface import AgentInterface
from task.task import Task


class Action(ABC):
    @abstractmethod
    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        """Execute the action given a task and a reason."""
