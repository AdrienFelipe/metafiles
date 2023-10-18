from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.prompt_factory import PromptFactory
from task import Task


def test_create_code_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.filter_requirements(task, "sub goal")
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)
