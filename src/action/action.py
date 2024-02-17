from abc import ABC, abstractmethod

from action.action_registry_interface import IActionRegistry
from action.action_result import ActionResult
from agent.agent_interface import AgentInterface
from core.service.service_container import ServiceContainer
from task.task import Task
from task.task_handler_interface import ITaskHandler


class Action(ABC):
    def __init__(self, container: ServiceContainer):
        self._container = container
        self._task_handler = container.get_service(ITaskHandler)
        self._action_registry = container.get_service(IActionRegistry)

    @abstractmethod
    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        """Execute the action given a task and a reason."""
