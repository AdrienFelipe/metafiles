from abc import ABC

from agent_config import AgentConfig
from agent_interface import AgentInterface
from prompt_result import PromptCallbackResponse, PromptResponse, PromptStatus
from prompts.prompt import Prompt


class BaseAgent(AgentInterface, ABC):
    def __init__(self, config: AgentConfig):
        self.config = config

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
