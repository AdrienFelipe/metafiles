import json
import os

import openai

from agent.agent_base import BaseAgent
from agent.agent_config import ModelType
from prompt.prompt import Prompt
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse, PromptResponse


class OpenAIAgent(BaseAgent):
    MODEL_MAP = {
        ModelType.FAST: "gpt-3.5-turbo",
        ModelType.CAPABLE: "gpt-4",
    }

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        super().__init__()

    def send_query(self, prompt: Prompt) -> PromptResponse:
        config = prompt.strategy.agent_config()
        args = {
            "model": OpenAIAgent.MODEL_MAP[config.model],
            "messages": prompt.messages(),
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        }

        functions_value = prompt.functions()
        if functions_value:
            args["functions"] = functions_value
            args["function_call"] = prompt.callback()

        return openai.ChatCompletion.create(**args)

    def parse_response(self, response) -> PromptResponse:
        message = response.choices[0].message
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function_arguments = json.loads(message["function_call"]["arguments"])
            return PromptCallbackResponse(function_name, function_arguments)
        else:
            return PromptMessageResponse(message["content"])