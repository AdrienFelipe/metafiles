from abc import ABC, abstractmethod

from prompt_result import PromptResponse


class AgentInterface(ABC):
    @abstractmethod
    def send(self, prompt: str):
        pass

    @abstractmethod
    def parseResponse(self, response) -> PromptResponse:
        pass
