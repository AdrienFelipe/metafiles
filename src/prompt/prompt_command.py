from abc import ABC, abstractmethod
from typing import Generic

from action.action_registry_interface import IActionRegistry
from agent.agent_interface import AgentInterface
from core.service.service_container import ServiceContainer
from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse, TPromptResponse
from prompt.prompt_strategy import TStrategy
from task.task import Task
from task.task_handler_interface import ITaskHandler


class PromptCommand(ABC, Generic[TStrategy]):
    strategy: TStrategy

    def __init__(self, container: ServiceContainer, agent: AgentInterface, task: Task) -> None:
        # self._container = container
        self._action_registry = container.get_service(IActionRegistry)
        self._task_handler = container.get_service(ITaskHandler)
        self.agent = agent
        self.task = task
        self.strategy = self._define_strategy()

    def _ask_agent(self) -> PromptResponse:
        prompt = Prompt(self.task, self.strategy)
        return self.agent.ask(prompt)

    @abstractmethod
    def _define_strategy(self) -> TStrategy:
        """
        Subclasses should implement this method to define their strategy.
        """

    @staticmethod
    def _error_message(response: PromptResponse) -> str:
        return f"Unexpected response type: {type(response)} - {response.message}"


class PromptCommandResult(Generic[TStrategy, TPromptResponse]):
    def __init__(self, strategy: TStrategy, response: TPromptResponse, task: Task) -> None:
        self.strategy: TStrategy = strategy
        self.response: TPromptResponse = response
        self.task: Task = task
