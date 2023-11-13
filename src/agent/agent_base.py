from abc import ABC
from typing import Union

from agent.agent_interface import AgentInterface
from prompt.prompt import Prompt
from prompt.prompt_result import FailedPromptResponse, PromptCallbackResponse, PromptResponse
from prompt.prompt_strategy import IPromptStrategy


class BaseAgent(AgentInterface, ABC):
    def ask(self, prompt: Prompt[IPromptStrategy]) -> Union[PromptResponse, FailedPromptResponse]:
        try:
            response = self.parse_response(self.send_query(prompt))
            return self._handle_response(prompt, response)
        except Exception as e:
            return FailedPromptResponse(f"Error parsing response: {e}")

    def _handle_response(self, prompt: Prompt[IPromptStrategy], parsed_response: PromptResponse) -> PromptResponse:
        if isinstance(parsed_response, PromptCallbackResponse):
            handler = prompt.strategy.handler_functions().get(parsed_response.get_function_name())
            if handler:
                try:
                    return handler(prompt.task, **parsed_response.get_function_arguments())
                except Exception as e:
                    return FailedPromptResponse(f"Error in callback function: {e}")
            else:
                message = (
                    f"Agent chose a non-defined function: {parsed_response.get_function_name()}"
                )
                print(message)
                return FailedPromptResponse(message)

        return parsed_response
