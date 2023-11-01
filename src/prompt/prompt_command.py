from abc import ABC, abstractmethod

from action.action_name import ActionName
from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from prompt.callbacks.query_user import QueryUserResponse
from prompt.prompt_result import PromptResponse
from task.task import Task


class PromptCommand(ABC):
    @staticmethod
    @abstractmethod
    def ask(agent: AgentInterface) -> PromptResponse:
        pass

    @staticmethod
    def _error_message(response: PromptResponse) -> str:
        return f"Unexpected response type: {type(response)} - {response.message}"

    @staticmethod
    def _ask_user(agent: AgentInterface, task: Task, query: str) -> QueryUserResponse:
        return action_registry.get_action(ActionName.ASK_USER).execute(agent, task, query)
