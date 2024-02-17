from action.action_name import ActionName
from prompt.callbacks.code import (
    CreateCodeResponse,
    FailedCreateCodeResponse,
    NoCodeResponse,
    ValidateCodeResponse,
)
from prompt.callbacks.query_user import QueryUserResponse
from prompt.callbacks.task import (
    AddTaskDependenciesResponse,
    DivideTaskResponse,
    ExecuteTaskResponse,
)
from prompt.prompt_command import PromptCommand
from prompt.prompt_result import PromptMessageResponse
from prompt.strategies.create_code import CreateCodeStrategy

MAX_ITERATIONS = 20


class CreateCodeCommand(PromptCommand[CreateCodeStrategy]):
    def ask(self, reason: str = "") -> CreateCodeResponse:
        self.strategy.set_reason(reason)
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS:
            response = self._ask_agent()
            if isinstance(response, (CreateCodeResponse, ValidateCodeResponse)):
                return response
            elif isinstance(response, QueryUserResponse):
                answer = self._action_registry.get_action(ActionName.ASK_USER).execute(
                    self.agent, self.task, response.query()
                )
                self.strategy.add_query(response.query(), answer.message)
            elif isinstance(response, AddTaskDependenciesResponse):
                self.task.add_dependencies(response.tasks())
                for task in response.tasks():
                    if not task.result.is_completed():
                        self._task_handler.execute(self.agent, task)
            elif isinstance(response, ExecuteTaskResponse):
                self._task_handler.execute(self.agent, response.task(), response.reason())
            elif isinstance(response, DivideTaskResponse):
                self.task.action = ActionName.DIVIDE_TASK
                return NoCodeResponse(response.reason())
            elif isinstance(response, PromptMessageResponse):
                self.strategy.add_message(response.get_message())
            # TODO: handle non expected responses

            iteration_count += 1

        return FailedCreateCodeResponse(PromptCommand._error_message(response))

    def _define_strategy(self) -> CreateCodeStrategy:
        return CreateCodeStrategy()
