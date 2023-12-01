from agent.agents.fake_agent import FakeAgent
from core.logger.no_logger import NoLogger
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.prompt import Prompt
from prompt.strategies.review_result import ReviewResultStrategy
from task.task import Task


def test_review_result_callbacks():
    task = Task("test", "test")
    prompt = Prompt(task, ReviewResultStrategy())
    assert_prompt_callbacks_are_valid(FakeAgent(NoLogger()), prompt)
