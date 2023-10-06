# openai_chat.py

import openai
import os

class OpenAIChat:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_chat_completion(self, messages, functions=[], function_call=None, temperature=0, max_tokens=2048):
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call=function_call,
            temperature=temperature,
            max_tokens=max_tokens
        )
