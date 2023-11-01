from typing import Dict, List, Optional, Type

from agent.agent_base import BaseAgent
from prompt.prompt import Prompt
from prompt.prompt_result import PromptMessageResponse, PromptResponse
from prompt.prompt_strategy import IPromptStrategy


class FakeAgent(BaseAgent):
    default_response = PromptMessageResponse("Default response")
    responses: Dict[Type[IPromptStrategy], List[PromptResponse]] = {}

    def __init__(self, responses: Optional[List[PromptResponse]] = None):
        if responses is not None:
            self.add_responses(responses)

    def add_responses(self, responses: List[PromptResponse]) -> None:
        self.responses.setdefault(IPromptStrategy, []).extend(responses)

    def add_strategy_responses(
        self, responses: Dict[Type[IPromptStrategy], List[PromptResponse]]
    ) -> None:
        for strategy, strategy_responses in responses.items():
            self.responses.setdefault(strategy, []).extend(strategy_responses)

    def send_query(self, prompt: Prompt) -> PromptResponse:
        responses = self.responses.get(type(prompt.strategy), self.responses.get(IPromptStrategy))
        if not responses:
            return self.default_response

        return responses.pop(0) if len(responses) > 1 else responses[0]

    def parse_response(self, response) -> PromptResponse:
        return response
