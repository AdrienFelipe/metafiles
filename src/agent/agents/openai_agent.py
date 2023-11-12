import json
import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from agent.agent_base import BaseAgent
from agent.agent_config import ModelType
from prompt.prompt import Prompt
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse, PromptResponse
from prompt.prompt_strategy import IPromptStrategy


class OpenAIAgent(BaseAgent):
    MODEL_MAP = {
        ModelType.FAST: "gpt-3.5-turbo",
        ModelType.CAPABLE: "gpt-4",
    }

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        super().__init__()

    def send_query(self, prompt: Prompt[IPromptStrategy]) -> PromptResponse:
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

        return self.client.chat.completions.create(**args)

    def parse_response(self, response: ChatCompletion) -> PromptResponse:
        message = response.choices[0].message
        if message.function_call is not None:
            function_name = message.function_call.name
            function_arguments = json.loads(message.function_call.arguments)
            return PromptCallbackResponse(function_name, function_arguments)
        else:
            return PromptMessageResponse(message.content)
