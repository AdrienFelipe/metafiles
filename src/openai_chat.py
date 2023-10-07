import json
import os

import openai

from prompt_result import PromptResponse, PromptStatus
from prompts.prompt import Prompt


class OpenAIChat:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def ask(self, prompt: Prompt):
        return self._handle(prompt, self._send(prompt))

    def _send(self, prompt: Prompt):
        print("-------")
        print(prompt.messages())
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt.messages(),
            functions=prompt.functions(),
            function_call=prompt.callback(),
            temperature=0,
            max_tokens=2048,
        )

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
            return PromptResponse(PromptStatus.SUCCESS, message["content"])
