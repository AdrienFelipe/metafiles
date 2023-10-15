from abc import ABC

from agent.agent_interface import AgentInterface
from prompt.prompt import Prompt
from prompt.prompt_result import PromptCallbackResponse, PromptResponse, PromptStatus


class BaseAgent(AgentInterface, ABC):
    def ask(self, prompt: Prompt):
        response = self.parse_response(self.send_query(prompt))
        return self._handle_response(prompt, response)

    def _handle_response(self, prompt: Prompt, parsed_response: PromptResponse) -> PromptResponse:
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
