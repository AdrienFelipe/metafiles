from agent.agents.test_agent import TestAgent
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task import Task


def test_agent_base_undefined_callback():
    task = Task("test", "test")
    prompt = PromptFactory.choose_action(task)

    responses = [PromptCallbackResponse("not_set_callback", {"test": "test"})]
    agent = TestAgent(responses)

    assert not agent.ask(
        prompt
    ).is_successful(), "Expected response to be unsuccessful but it was successful."
