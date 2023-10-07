from typing import List

from callbacks import (
    ChooseActionResponse,
    ChooseAgentResponse,
    CreatePlanResponse,
    QueryUserResponse,
    ValidatePlanResponse,
)
from openai_chat import OpenAIChat
from prompt_result import PromptMessageResponse
from prompts.prompt_factory import PromptFactory
from task import Task


class AgentProxy:
    def __init__(self, agent: OpenAIChat):
        self.agent = agent

    def ask_for_agent_roles(self, task: Task) -> List[str]:
        response = self.agent.ask(PromptFactory.choose_agent(task))
        if isinstance(response, ChooseAgentResponse):
            return response.roles
        raise UnexpectedResponseTypeError(type(response))

    def ask_to_choose_action(self, task: Task) -> (str, str):
        response = self.agent.ask(PromptFactory.choose_action(task))
        if isinstance(response, ChooseActionResponse):
            return response.action_key, response.reason
        raise UnexpectedResponseTypeError(type(response))

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
                raise UnexpectedResponseTypeError(type(response))

    def ask_user(self, query: str) -> str:
        return input(query)


class UnexpectedResponseTypeError(Exception):
    def __init__(self, actual_type):
        super().__init__(f"Unexpected response type: {actual_type}")
        self.actual_type = actual_type
