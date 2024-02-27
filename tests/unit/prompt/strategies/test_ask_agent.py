from agent.agents.fake_agent import FakeAgent
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from helpers.prompt_helper import assert_prompt_callbacks_are_valid
from prompt.commands.ask_agent_command import AskAgentCommand
from prompt.context.prompt_context_interface import IPromptContext
from prompt.prompt import Prompt
from prompt.prompt_result import PromptMessageResponse
from prompt.strategies.ask_agent import AskAgentStrategy
from task.task import Task


def test_ask_agent_callbacks(logger: IExecutionLogger, prompt_context: IPromptContext):
    parent_task = Task("Parent task", "Parent task definition")
    Task("Previous task 1", "Previous task 1 definition", parent=parent_task)
    Task("Previous task 2", "Previous task 2 definition", parent=parent_task)
    task = Task("Task goal", "Task definition", parent=parent_task)
    prompt = Prompt(task, AskAgentStrategy(), prompt_context)

    specials = {
        "tasks_ids": "0.0, 0.1",
        "task_id": "0.1",
    }
    assert_prompt_callbacks_are_valid(FakeAgent(logger), prompt, specials)


def test_ask_agent_with_prompt_message_response(
    container: ServiceContainer, logger: IExecutionLogger
):
    task = Task("Task goal", "Task definition")
    agent = FakeAgent(logger)
    message = "Agent response"
    agent.add_responses([PromptMessageResponse(message)])

    response = AskAgentCommand(container, agent, task).ask("role expert")
    assert not response.is_failure(), f"Response should not fail - {response.message}"
    assert response.get_message() == message, f"Invalid response message - {response.message}"
