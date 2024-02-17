from action.action_name import ActionName
from prompt.callbacks.ask_code import AskForCodeResponse
from prompt.callbacks.query_user import QueryUserResponse
from prompt.callbacks.task import AddTaskDependenciesResponse, ExecuteTaskResponse
from prompt.callbacks.validate_response import ValidateResponse
from prompt.prompt_command import PromptCommand
from prompt.prompt_result import (
    FailedPromptResponse,
    PostponeResponse,
    PromptMessageResponse,
    PromptResponse,
)
from prompt.strategies.ask_agent import AskAgentStrategy

MAX_ITERATIONS = 5


class AskAgentCommand(PromptCommand[AskAgentStrategy]):
    def ask(self, role: str) -> PromptResponse:
        self.strategy.set_role(role)
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS:
            response = self._ask_agent()
            if isinstance(response, (PromptMessageResponse, ValidateResponse)):
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
            elif isinstance(response, AskForCodeResponse):
                self.task.action = ActionName.RUN_CODE
                return PostponeResponse(response.reason())
            else:
                self.strategy.add_message(PromptCommand._error_message(response))

            iteration_count += 1

        return FailedPromptResponse(PromptCommand._error_message(response))

    def _define_strategy(self) -> AskAgentStrategy:
        return AskAgentStrategy()
