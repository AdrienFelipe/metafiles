from abc import ABC, abstractmethod

from agent.agent_config import AgentConfig
from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse


class AgentInterface(ABC):
    @abstractmethod
    def send(self, config: AgentConfig, prompt: Prompt):
        pass

    @abstractmethod
    def parse_response(self, response) -> PromptResponse:
        pass
