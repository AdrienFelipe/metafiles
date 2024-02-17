from abc import ABC, abstractmethod

from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse
from prompt.prompt_strategy import TStrategy


class AgentInterface(ABC):
    @abstractmethod
    def ask(self, prompt: Prompt[TStrategy]) -> PromptResponse:
        pass

    @abstractmethod
    def send_query(self, prompt: Prompt[TStrategy]):
        pass

    @abstractmethod
    def parse_response(self, response) -> PromptResponse:
        pass

    @abstractmethod
    def logger(self):
        pass
