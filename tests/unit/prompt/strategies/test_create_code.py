from agent.agent_proxy import AgentProxy
from agent.agents.fake_agent import FakeAgent
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.callbacks.code import CreateCodeResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task.task import Task


def test_create_code_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.create_code(task, "reason")
    assert_prompt_callbacks_are_valid(FakeAgent(), prompt)


def test_create_code_agent_proxy_success():
    code = "var = 'ok'\nreturn var"
    arguments = {"code": code, "test_args": "{}", "tasks_ids": "", "update_reason": ""}
    agent = FakeAgent([PromptCallbackResponse("execute_code", arguments)])
    agent_proxy, task = AgentProxy(agent), Task("test", "test")

    response = agent_proxy.ask_for_code(task)
    assert isinstance(response, CreateCodeResponse)
    assert response.is_successful(), "Response should be successful"
    assert response.get_code() == code, "Incorrect code"
