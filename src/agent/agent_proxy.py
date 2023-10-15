from typing import List, Tuple

from action.action_name import ActionName
from agent.agent_interface import AgentInterface
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
    def __init__(self, agent: AgentInterface):
        self.agent = agent

    def ask_for_agent_roles(self, task: Task) -> List[str]:
        response = self.agent.ask(PromptFactory.choose_agent(task))
        if isinstance(response, ChooseAgentResponse):
            return response.roles
        raise UnexpectedResponseTypeException(type(response))

    def ask_to_choose_action(self, task: Task) -> Tuple[ActionName, str]:
        response = self.agent.ask(PromptFactory.choose_action(task))
        if isinstance(response, ChooseActionResponse):
            if response.action_key not in ActionName._value2member_map_:
                raise InvalidResponseArgumentException(f"action name: {response.action_key}")
            return ActionName(response.action_key), response.reason

        raise UnexpectedResponseTypeException(type(response))

    def ask_to_create_plan(self, task: Task, role: str) -> List[str]:
        prompt = PromptFactory.create_plan(task, role)

        while True:
            response = self.agent.ask(prompt)

            if isinstance(response, (CreatePlanResponse, ValidatePlanResponse)):
                return response.plan_lines
            elif isinstance(response, QueryUserResponse):
                user_response = self.ask_user(response.query)
                prompt.add_message("assistant", response.query)
                prompt.add_message("user", user_response)
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.message)
            else:
                raise UnexpectedResponseTypeException(type(response))

    def ask_to_filter_requirements(self, task: Task, sub_goal: str) -> str:
        response = self.agent.ask(PromptFactory.filter_requirements(task, sub_goal))
        if isinstance(response, PromptMessageResponse):
            return response.message
        raise UnexpectedResponseTypeException(type(response))

    def ask_for_code(self, task: Task, reason: str) -> str:
        response = self.agent.ask(PromptFactory.create_code(task, reason))
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
