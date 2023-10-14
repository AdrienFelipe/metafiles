from abc import ABC, abstractmethod
from enum import Enum

from action_result import ActionResult
from agent_interface import AgentInterface
from task import Task


class ActionName(Enum):
    ASK_AGENT = "ask_agent"
    ASK_USER = "ask_user"
    RUN_CODE = "run_code"
    DIVIDE_TASK = "divide_task"


class Action(ABC):
    @abstractmethod
    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        """Execute the action given a task and a reason."""
