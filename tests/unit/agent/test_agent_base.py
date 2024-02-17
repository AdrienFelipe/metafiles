from agent.agents.fake_agent import FakeAgent
from core.logger.logger_interface import IExecutionLogger
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task.task import Task


def test_agent_base_undefined_callback(logger: IExecutionLogger):
    task = Task("test", "test")
    prompt = PromptFactory.choose_action(task)

    responses = [PromptCallbackResponse("not_set_callback", {"test": "test"})]
    agent = FakeAgent(logger, responses)

    assert not agent.ask(
        prompt
    ).is_ok(), "Expected response to be unsuccessful but it was successful."
