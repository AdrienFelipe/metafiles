from typing import Union

from agent.agent_interface import AgentInterface
from core.logger.logger_interface import IExecutionLogger
from prompt.prompt import Prompt
from prompt.prompt_result import FailedPromptResponse, PromptCallbackResponse, PromptResponse
from prompt.prompt_strategy import IPromptStrategy


class BaseAgent(AgentInterface):
    def __init__(self, logger: IExecutionLogger) -> None:
        self._logger = logger

    def logger(self):
        return self._logger

    def ask(self, prompt: Prompt[IPromptStrategy]) -> Union[PromptResponse, FailedPromptResponse]:
        try:
            self._logger.log(
                "➡️ Sending prompt", {"strategy": prompt.strategy, "prompt": prompt.messages()}
            )
            raw_response = self.send_query(prompt)

            parsed_response = self.parse_response(raw_response)
            self._logger.log("⬅️ Agent response", {"response": parsed_response})

            response = self._handle_response(prompt, parsed_response)
            self._logger.log(f"🔄 Handled response: '{type(response).__name__}'")

            return response
        except Exception as e:
            self._logger.log(f"💥 Error: {e}")
            return FailedPromptResponse(f"Error parsing response: {e}")

    def _handle_response(
        self, prompt: Prompt[IPromptStrategy], response: PromptResponse
    ) -> PromptResponse:
        if isinstance(response, PromptCallbackResponse):
            callback = prompt.strategy.callbacks().get(response.callback_name())
            if callback:
                try:
                    return callback(prompt.task, **response.callback_arguments())
                except Exception as e:
                    return FailedPromptResponse(f"Error in callback function: {e}")
            else:
                message = f"Agent chose a non-defined function: {response.callback_name()}"
                print(message)
                return FailedPromptResponse(message)

        return response
