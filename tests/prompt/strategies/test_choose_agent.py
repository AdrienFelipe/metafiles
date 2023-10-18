from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.prompt_factory import PromptFactory
from task import Task


def test_choose_agent_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.choose_agent(task)
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)
