from action.action_name import ActionName
from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from prompt.callbacks.choose_action import ChooseActionResponse, FailedChooseActionResponse
from prompt.callbacks.choose_agent import ChooseAgentResponse, FailedChooseAgentResponse
from prompt.callbacks.code import CreateCodeResponse
from prompt.callbacks.plan import CreatePlanResponse, FailedCreatePlanResponse, ValidatePlanResponse
from prompt.callbacks.query_user import QueryUserResponse
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptMessageResponse, PromptResponse
from task import Task


class AgentProxy:
    def __init__(self, agent: AgentInterface):
        self.agent = agent

    def __error_message(self, response: PromptResponse) -> str:
        return f"Unexpected response type: {type(response)} - {response.message}"

    def ask_for_agent_roles(self, task: Task) -> ChooseAgentResponse:
        response = self.agent.ask(PromptFactory.choose_agent(task))
        if isinstance(response, ChooseAgentResponse):
            return response

        return FailedChooseAgentResponse(self.__error_message(response))

    def ask_to_choose_action(self, task: Task) -> ChooseActionResponse:
        response = self.agent.ask(PromptFactory.choose_action(task))
        if isinstance(response, ChooseActionResponse):
            return response

        return FailedChooseActionResponse(self.__error_message(response))

    def ask_to_create_plan(self, task: Task, role: str) -> CreatePlanResponse:
        prompt = PromptFactory.create_plan(task, role)

        # TODO: add maximum number of retries
        while True:
            response = self.agent.ask(prompt)

            if isinstance(response, (CreatePlanResponse, ValidatePlanResponse)):
                return response
            elif isinstance(response, QueryUserResponse):
                action = action_registry.get_action(ActionName.ASK_USER)
                user_response = action.execute(self.agent, task, response.get_query())

                prompt.add_message("assistant", response.get_query())
                prompt.add_message("user", user_response.message)
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.message)
            else:
                return FailedCreatePlanResponse(self.__error_message(response))

    def ask_to_filter_requirements(self, task: Task, sub_goal: str) -> str:
        response = self.agent.ask(PromptFactory.filter_requirements(task, sub_goal))
        if isinstance(response, PromptMessageResponse):
            return response.message
        raise UnexpectedResponseTypeException(type(response))

    def ask_for_code(self, task: Task, reason: str) -> str:
        response = self.agent.ask(PromptFactory.create_code(task, reason))
        if isinstance(response, CreateCodeResponse):
            return response.get_code()
        raise UnexpectedResponseTypeException(type(response))


class UnexpectedResponseTypeException(Exception):
    def __init__(self, actual_type):
        super().__init__(f"Unexpected response type: {actual_type}")
        self.actual_type = actual_type


class InvalidResponseArgumentException(Exception):
    def __init__(self, argument_name):
        super().__init__(f"Invalid response argument: {argument_name}")
        self.argument_name = argument_name
