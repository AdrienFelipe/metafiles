from abc import ABC, abstractmethod
from typing import Generic

from action.action_registry_interface import IActionRegistry
from agent.agent_interface import AgentInterface
from core.service.service_container import ServiceContainer
from prompt.context.prompt_context_interface import IPromptContext
from prompt.prompt import Prompt
from prompt.prompt_result import FailedPromptResponse, PromptResponse, TPromptResponse
from prompt.prompt_strategy import TStrategy
from task.task import Task
from task.task_handler_interface import ITaskHandler


class PromptCommand(ABC, Generic[TStrategy]):
    strategy: TStrategy

    def __init__(self, container: ServiceContainer, agent: AgentInterface, task: Task) -> None:
        # self._container = container
        self._action_registry = container.get_service(IActionRegistry)
        self._task_handler = container.get_service(ITaskHandler)
        self._context = container.get_service(IPromptContext)

        self.agent = agent
        self.task = task
        self.strategy = self._define_strategy()

    def _ask_agent(self) -> PromptResponse:
        prompt = Prompt(self.task, self.strategy, self._context)

        try:
            response = self.agent.ask(prompt)
        except Exception as e:
            response = FailedPromptResponse(str(e))
        self._context.add_agent_query(prompt, response)
        
        return response

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
