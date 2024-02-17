from abc import abstractmethod

from agent.agent_interface import AgentInterface
from core.service.service_type import IService
from task.task import Task


class ITaskHandler(IService):
    @abstractmethod
    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> None:
        raise NotImplementedError
