from prompt.callbacks.review_result import FailedReviewResultResponse, ReviewResultResponse
from prompt.prompt_command import PromptCommand
from prompt.strategies.review_result import ReviewResultStrategy

MAX_ITERATIONS = 3


class ReviewResultCommand(PromptCommand[ReviewResultStrategy]):
    def ask(self) -> ReviewResultResponse:
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS:
            response = self._ask_agent()
            if isinstance(response, ReviewResultResponse):
                return response

            self.strategy.add_message(self._error_message(response))
            iteration_count += 1

        return FailedReviewResultResponse("Max iterations reached")

    def _define_strategy(self) -> ReviewResultStrategy:
        return ReviewResultStrategy()
