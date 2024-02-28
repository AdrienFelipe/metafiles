from action.action_name import ActionName
from action.action_registry_interface import IActionRegistry
from action.action_result import ActionResult
from agent.agent_interface import AgentInterface
from core.service.service_container import ServiceContainer
from prompt.callbacks.choose_action import ChooseActionResponse, FailedChooseActionResponse
from prompt.callbacks.choose_agent import ChooseAgentResponse, FailedChooseAgentResponse
from prompt.callbacks.plan import CreatePlanResponse, FailedCreatePlanResponse, ValidatePlanResponse
from prompt.callbacks.query_user import QueryUserResponse
from prompt.context.prompt_context_interface import IPromptContext
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptMessageResponse, PromptResponse
from task.task import Task


class AgentProxy:
    def __init__(self, container: ServiceContainer, agent: AgentInterface):
        self._action_registry = container.get_service(IActionRegistry)
        self._context = container.get_service(IPromptContext)

        self.agent = agent

    def __error_message(self, response: PromptResponse) -> str:
        return f"Unexpected response type: {type(response)} - {response.message}"

    def ask_for_agent_roles(self, task: Task, reason: str = "") -> ChooseAgentResponse:
        response = self.agent.ask(PromptFactory.choose_agent(task, self._context, reason))
        if isinstance(response, ChooseAgentResponse):
            return response

        return FailedChooseAgentResponse(self.__error_message(response))

    def ask_to_choose_action(self, task: Task, reason: str = "") -> ChooseActionResponse:
        prompt = PromptFactory.choose_action(task, self._context, reason)
        response = self.agent.ask(prompt)
        self._context.add_agent_query(prompt, response)

        if isinstance(response, ChooseActionResponse):
            return response

        return FailedChooseActionResponse(self.__error_message(response))

    def ask_to_create_plan(self, task: Task, role: str, reason: str = "") -> CreatePlanResponse:
        prompt = PromptFactory.create_plan(task, self._context, role, reason)

        # TODO: add maximum number of retries
        while True:
            response = self.agent.ask(prompt)

            if isinstance(response, (CreatePlanResponse, ValidatePlanResponse)):
                return response
            elif isinstance(response, QueryUserResponse):
                user_response = self.query_user(task, response.query())
                prompt.add_message("assistant", response.query())
                prompt.add_message("user", user_response.message)
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.message)
            else:
                return FailedCreatePlanResponse(self.__error_message(response))

    def query_user(self, task: Task, query: str) -> ActionResult:
        action = self._action_registry.get_action(ActionName.ASK_USER)
        return action.execute(self.agent, task, query)


class UnexpectedResponseTypeException(Exception):
    def __init__(self, actual_type):
        super().__init__(f"Unexpected response type: {actual_type}")
        self.actual_type = actual_type
