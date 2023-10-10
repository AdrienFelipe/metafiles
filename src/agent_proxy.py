from typing import List

from callbacks import (
    ChooseActionResponse,
    ChooseAgentResponse,
    CreatePlanResponse,
    QueryUserResponse,
    ValidatePlanResponse,
)
from prompt_result import PromptMessageResponse
from prompts.prompt_factory import PromptFactory
from task import Task


class AgentProxy:
    @staticmethod
    def ask_for_agent_roles(task: Task) -> List[str]:
        response = PromptFactory.choose_agent(task).ask()
        if isinstance(response, ChooseAgentResponse):
            return response.roles
        raise UnexpectedResponseTypeError(type(response))

    @staticmethod
    def ask_to_choose_action(task: Task) -> (str, str):
        response = PromptFactory.choose_action(task).ask()
        if isinstance(response, ChooseActionResponse):
            return response.action_key, response.reason
        raise UnexpectedResponseTypeError(type(response))

    @staticmethod
    def ask_to_create_plan(task: Task, role: str) -> List[str]:
        prompt = PromptFactory.create_plan(task, role)

        while True:
            response = prompt.ask()

            if isinstance(response, (CreatePlanResponse, ValidatePlanResponse)):
                return response.plan_lines
            elif isinstance(response, QueryUserResponse):
                user_response = AgentProxy.ask_user(response.query)
                prompt.add_message("assistant", response.query)
                prompt.add_message("user", user_response)
            elif isinstance(response, PromptMessageResponse):
                prompt.add_message("assistant", response.message)
            else:
                raise UnexpectedResponseTypeError(type(response))

    @staticmethod
    def ask_to_filter_requirements(task: Task, sub_goal: str) -> str:
        response = PromptFactory.filter_requirements(task, sub_goal).ask()
        if isinstance(response, PromptMessageResponse):
            return response.message
        raise UnexpectedResponseTypeError(type(response))

    def ask_user(self, query: str) -> str:
        return input(query)


class UnexpectedResponseTypeError(Exception):
    def __init__(self, actual_type):
        super().__init__(f"Unexpected response type: {actual_type}")
        self.actual_type = actual_type
