from abc import ABC, abstractmethod

from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse


class AgentInterface(ABC):
    @abstractmethod
    def ask(self, prompt: Prompt) -> PromptResponse:
        pass

    @abstractmethod
    def send_query(self, prompt: Prompt):
        pass

    @abstractmethod
    def parse_response(self, response) -> PromptResponse:
        pass
