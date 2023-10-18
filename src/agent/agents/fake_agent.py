from typing import List, Optional

from agent.agent_base import BaseAgent
from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse


class FakeAgent(BaseAgent):
    def __init__(self, responses: Optional[List[PromptResponse]] = None):
        self.responses = responses if responses is not None else []

    def add_responses(self, responses: List[PromptResponse]) -> None:
        self.responses.extend(responses)

    def send_query(self, prompt: Prompt) -> PromptResponse:
        return self.responses.pop(0)

    def parse_response(self, response) -> PromptResponse:
        return response
