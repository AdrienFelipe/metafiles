import json
import openai
import os

from prompts.prompt import Prompt


class OpenAIChat:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def ask(self, prompt: Prompt):
        return self._handle(prompt, self._send(prompt))

    def _send(self, prompt: Prompt):
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt.messages(),
            functions=prompt.functions(),
            function_call={"name": prompt.callback()},
            temperature=0,
            max_tokens=2048,
        )

    def _handle(self, prompt: Prompt, response):
        message = response.choices[0].message
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function_arguments = json.loads(message["function_call"]["arguments"])

            handler = prompt.strategy.get_handler_function(
                function_name
            )  # We fetch handler function using strategy
            if handler:
                return handler(prompt.task, **function_arguments)
            else:
                print("Agent chose a non-defined function:", function_name)
                return False
        else:
            print(message["content"])
            return False
