import json
import os

import openai

from agent_interface import AgentInterface
from prompt_result import PromptMessageResponse, PromptResponse, PromptStatus
from prompts.prompt import Prompt


class OpenAIAgent(AgentInterface):
    def __init__(self, model: str, max_tokens: int = 2048, temperature: int = 0):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    def ask(self, prompt: Prompt):
        return self._handle(prompt, self._send(prompt))

    def _send(self, prompt: Prompt):
        args = {
            "model": self._model,
            "messages": prompt.messages(),
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }

        functions_value = prompt.functions()
        if functions_value:
            args["functions"] = functions_value
            args["function_call"] = prompt.callback()

        return openai.ChatCompletion.create(**args)

    def _handle(self, prompt: Prompt, response) -> PromptResponse:
        message = response.choices[0].message
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function_arguments = json.loads(message["function_call"]["arguments"])

            handler = prompt.strategy.handler_functions().get(function_name)
            if handler:
                return handler(prompt.task, **function_arguments)
            else:
                print("Agent chose a non-defined function:", function_name)
                return PromptResponse(
                    PromptStatus.FAILURE, f"Agent chose a non-defined function: {function_name}"
                )
        else:
            return PromptMessageResponse(message["content"])
