import json
import os

import openai

from agent_base import BaseAgent
from prompt_result import PromptCallbackResponse, PromptMessageResponse, PromptResponse
from prompts.prompt import Prompt


class OpenAIAgent(BaseAgent):
    def __init__(self, model: str, max_tokens: int = 2048, temperature: int = 0):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        super().__init__(model, max_tokens, temperature)

    def send(self, prompt: Prompt):
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

    def parseResponse(self, response) -> "PromptResponse":
        message = response.choices[0].message
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function_arguments = json.loads(message["function_call"]["arguments"])
            return PromptCallbackResponse(function_name, function_arguments)
        else:
            return PromptMessageResponse(message["content"])
