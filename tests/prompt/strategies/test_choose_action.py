from agent.agents.test_agent import TestAgent
from helpers.prompt_helper import prompt_function_to_callback_arguments
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptCallbackResponse
from task import Task


def test_choose_action_callbacks():
    task = Task("test", "test")
    prompt = PromptFactory.choose_action(task)
    agent = TestAgent()

    for function in prompt.functions():
        callback = function["name"]
        arguments = prompt_function_to_callback_arguments(function)
        agent.add_responses([PromptCallbackResponse(callback, arguments)])

        assert agent.ask(prompt).is_successful()
