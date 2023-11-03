from abc import ABC

from prompt.prompt_result import PromptResponse


class PromptCommand(ABC):
    @staticmethod
    def _error_message(response: PromptResponse) -> str:
        return f"Unexpected response type: {type(response)} - {response.message}"
