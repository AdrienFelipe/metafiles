from action.action_name import ActionName
from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from prompt.callbacks.code import (
    CreateCodeResponse,
    FailedCreateCodeResponse,
    NoCodeResponse,
    ValidateCodeResponse,
)
from prompt.callbacks.query_user import QueryUserResponse
from prompt.callbacks.task import DivideTaskResponse, ExecuteTaskResponse, GetTasksResultsResponse
from prompt.prompt_command import PromptCommand
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptMessageResponse
from task.task import Task
from task.task_execute import execute_task

MAX_ITERATIONS = 20


class CreateCodeCommand(PromptCommand):
    @staticmethod
    def ask(agent: AgentInterface, task: Task, reason: str = "") -> CreateCodeResponse:
        prompt = PromptFactory.create_code(task, reason)
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS:
            response = agent.ask(prompt)
            if isinstance(response, (CreateCodeResponse, ValidateCodeResponse)):
                return response
            elif isinstance(response, QueryUserResponse):
                answer = action_registry.get_action(ActionName.ASK_USER).execute(
                    agent, task, response.query()
                )
                prompt.strategy.add_query(response.query(), answer.message)
            elif isinstance(response, GetTasksResultsResponse):
                prompt.strategy.add_dependencies(response.tasks())
            elif isinstance(response, ExecuteTaskResponse):
                execute_task(agent, response.task(), response.reason())
            elif isinstance(response, DivideTaskResponse):
                task.action = ActionName.DIVIDE_TASK
                return NoCodeResponse(response.reason())
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.get_message())
            else:
                return FailedCreateCodeResponse(PromptCommand._error_message(response))
