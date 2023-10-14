from typing import List, Tuple

from action.action import ActionName
from prompt.prompt_callbacks import (
    ChooseActionResponse,
    ChooseAgentResponse,
    CreateCodeResponse,
    CreatePlanResponse,
    QueryUserResponse,
    ValidatePlanResponse,
)
from prompt.prompt_factory import PromptFactory
from prompt.prompt_result import PromptMessageResponse
from task import Task


class AgentProxy:
    def __init__(self, agent):
        self.agent = agent

    def ask_for_agent_roles(self, task: Task) -> List[str]:
        response = PromptFactory.choose_agent(task).ask(self.agent)
        if isinstance(response, ChooseAgentResponse):
            return response.roles
        raise UnexpectedResponseTypeException(type(response))

    def ask_to_choose_action(self, task: Task) -> Tuple[ActionName, str]:
        response = PromptFactory.choose_action(task).ask(self.agent)
        if isinstance(response, ChooseActionResponse):
            if response.action_key not in ActionName._value2member_map_:
                raise InvalidResponseArgumentException(f"action name: {response.action_key}")
            return ActionName(response.action_key), response.reason

        raise UnexpectedResponseTypeException(type(response))

    def ask_to_create_plan(self, task: Task, role: str) -> List[str]:
        prompt = PromptFactory.create_plan(task, role)

        while True:
            response = prompt.ask(self.agent)

            if isinstance(response, (CreatePlanResponse, ValidatePlanResponse)):
                return response.plan_lines
            elif isinstance(response, QueryUserResponse):
                user_response = AgentProxy.ask_user(response.query)
                prompt.add_message("assistant", response.query)
                prompt.add_message("user", user_response)
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.message)
            else:
                raise UnexpectedResponseTypeException(type(response))

    def ask_to_filter_requirements(self, task: Task, sub_goal: str) -> str:
        response = PromptFactory.filter_requirements(task, sub_goal).ask(self.agent)
        if isinstance(response, PromptMessageResponse):
            return response.message
        raise UnexpectedResponseTypeException(type(response))

    def ask_for_code(self, task: Task, reason: str) -> str:
        response = PromptFactory.create_code(task, reason).ask(self.agent)
        if isinstance(response, CreateCodeResponse):
            return response.message
        raise UnexpectedResponseTypeException(type(response))

    def ask_user(self, query: str) -> str:
        return input(query)


class UnexpectedResponseTypeException(Exception):
    def __init__(self, actual_type):
        super().__init__(f"Unexpected response type: {actual_type}")
        self.actual_type = actual_type


class InvalidResponseArgumentException(Exception):
    def __init__(self, argument_name):
        super().__init__(f"Invalid response argument: {argument_name}")
        self.argument_name = argument_name
