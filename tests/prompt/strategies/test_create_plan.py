from agent.agents.test_agent import TestAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.prompt_factory import PromptFactory
from task import Task


def test_create_code_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.create_plan(task, "role")
    assert_prompt_callbacks_are_valid(TestAgent(), prompt)
