from typing import Dict, List, Optional, Sequence, Type

from agent.agent_base import BaseAgent
from core.logger.logger_interface import IExecutionLogger
from prompt.prompt import Prompt
from prompt.prompt_result import PromptMessageResponse, PromptResponse
from prompt.prompt_strategy import IPromptStrategy, TStrategy

DEFAULT_STRATEGY_KEY = object()


class FakeAgent(BaseAgent):
    default_response = PromptMessageResponse("Default response")

    def __init__(
        self,
        logger: IExecutionLogger,
        responses: Optional[Sequence[PromptResponse]] = None,
        keep_last: bool = False,
    ):
        super().__init__(logger)
        self.keep_last = keep_last
        self.responses: Dict[object, List[PromptResponse]] = {}
        if responses is not None:
            self.add_responses(responses)

    def add_responses(self, responses: Sequence[PromptResponse], reset: bool = False) -> None:
        if reset:
            self.responses[DEFAULT_STRATEGY_KEY] = list(responses)
        else:
            self.responses.setdefault(DEFAULT_STRATEGY_KEY, []).extend(responses)

    def add_strategy_responses(
        self, responses: Dict[Type[IPromptStrategy], List[PromptResponse]]
    ) -> None:
        for strategy, strategy_responses in responses.items():
            self.responses.setdefault(strategy, []).extend(strategy_responses)

    def send_query(self, prompt: Prompt[TStrategy]) -> PromptResponse:
        responses = self.responses.get(
            type(prompt.strategy), self.responses.get(DEFAULT_STRATEGY_KEY)
        )
        if not responses:
            return self.default_response

        return responses.pop(0) if not self.keep_last or len(responses) > 1 else responses[0]

    def parse_response(self, response) -> PromptResponse:
        return response
