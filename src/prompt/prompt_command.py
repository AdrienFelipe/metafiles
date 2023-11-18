from abc import ABC, abstractmethod
from typing import Generic

from agent.agent_interface import AgentInterface
from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse, TPromptResponse
from prompt.prompt_strategy import TStrategy
from task.task import Task


class PromptCommand(ABC, Generic[TStrategy]):
    strategy: TStrategy

    def __init__(self, agent: AgentInterface, task: Task) -> None:
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
