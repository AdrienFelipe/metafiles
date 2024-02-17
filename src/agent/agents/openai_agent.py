import json
import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from agent.agent_base import BaseAgent
from agent.agent_config import ModelType
from core.logger.logger_interface import IExecutionLogger
from prompt.prompt import Prompt
from prompt.prompt_result import PromptCallbackResponse, PromptMessageResponse, PromptResponse
from prompt.prompt_strategy import TStrategy


class OpenAIAgent(BaseAgent):
    MODEL_MAP = {
        ModelType.FAST: "gpt-3.5-turbo",
        ModelType.CAPABLE: "gpt-4-turbo-preview",
    }

    def __init__(self, logger: IExecutionLogger):
        super().__init__(logger)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def send_query(self, prompt: Prompt[TStrategy]) -> PromptResponse:
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

        return self.client.chat.completions.create(**args)  # type: ignore[call-overload]

    def parse_response(self, response: ChatCompletion) -> PromptResponse:
        message = response.choices[0].message
        if message.function_call is not None:
            function_name = message.function_call.name
            function_arguments_str = self.escape_response(message.function_call.arguments)
            function_arguments = json.loads(function_arguments_str)
            return PromptCallbackResponse(function_name, function_arguments)
        else:
            return PromptMessageResponse(message.content or "")

    # Escape newline and tab characters inside reponse if not yet escaped
    def escape_response(self, json_str):
        inside_string = False
        result = []
        i = 0

        while i < len(json_str):
            char = json_str[i]

            # Toggle inside_string flag when encountering an unescaped double quote
            if char == '"' and (i == 0 or json_str[i - 1] != "\\"):
                inside_string = not inside_string

            if inside_string:
                # Handle newline and tab characters inside a string
                if char == "\n":
                    result.append("\\n")
                elif char == "\t":
                    result.append("\\t")
                else:
                    result.append(char)
            else:
                result.append(char)

            i += 1

        return "".join(result)
