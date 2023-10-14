from abc import ABC, abstractmethod

from agent_config import AgentConfig
from prompt_result import PromptResponse
from prompts.prompt import Prompt


class AgentInterface(ABC):
    @abstractmethod
    def send(self, config: AgentConfig, prompt: Prompt):
        pass

    @abstractmethod
    def parse_response(self, response) -> PromptResponse:
        pass
