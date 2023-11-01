from action.action_name import ActionName
from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from prompt.callbacks.code import CreateCodeResponse, FailedCreateCodeResponse
from prompt.callbacks.query_user import QueryUserResponse
from prompt.callbacks.task import DivideTaskResponse, ExecuteTaskResponse, GetTasksResultsResponse
from prompt.prompt_command import PromptCommand
from prompt.prompt_factory import PromptFactory
from task.task import Task
from task.task_execute import execute_task


class CreateCodeCommand(PromptCommand):
    @staticmethod
    def ask(agent: AgentInterface, task: Task, reason: str = "") -> CreateCodeResponse:
        prompt = PromptFactory.create_code(task, reason)
        # TODO: add maximum number of retries
        while True:
            response = agent.ask(prompt)
            if isinstance(response, CreateCodeResponse):
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
                execute_task(agent, task, response.reason())
            else:
                return FailedCreateCodeResponse(PromptCommand._error_message(response))
