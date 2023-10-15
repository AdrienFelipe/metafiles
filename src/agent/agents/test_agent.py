from agent.agent_base import BaseAgent
from prompt.prompt import Prompt
from prompt.prompt_result import PromptMessageResponse, PromptResponse


class TestAgent(BaseAgent):
    def __init__(self, responses):
        self.responses = responses

    def send_query(self, prompt: Prompt) -> PromptResponse:
        response_content = self.responses.pop(0)
        return self.parse_response(response_content)

    def parse_response(self, response) -> PromptResponse:
        return PromptMessageResponse(response)
