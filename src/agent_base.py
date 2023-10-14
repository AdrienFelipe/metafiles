from abc import ABC

from agent_interface import AgentInterface
from prompt_result import PromptCallbackResponse, PromptResponse, PromptStatus
from prompts.prompt import Prompt


class BaseAgent(AgentInterface, ABC):
    def __init__(self, model: str, max_tokens: int = 2048, temperature: int = 0):
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    def ask(self, prompt: Prompt):
        response = self.send(prompt)
        parsed_response = self.parseResponse(response)
        return self._handle(prompt, parsed_response)

    def _handle(self, prompt: Prompt, parsed_response: PromptResponse) -> PromptResponse:
        if isinstance(parsed_response, PromptCallbackResponse):
            handler = prompt.strategy.handler_functions().get(parsed_response.get_function_name())
            if handler:
                return handler(prompt.task, **parsed_response.get_function_arguments())
            else:
                print(f"Agent chose a non-defined function: {parsed_response.get_function_name()}")
                return PromptResponse(
                    PromptStatus.FAILURE,
                    f"Agent chose a non-defined function: {parsed_response.get_function_name()}",
                )

        return parsed_response
