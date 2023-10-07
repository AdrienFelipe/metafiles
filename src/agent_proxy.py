from typing import Dict, List

from openai_chat import OpenAIChat
from prompts.prompt_factory import PromptFactory
from task import Task


class AgentProxy:
    def __init__(self, agent: OpenAIChat):
        self.agent = agent

    def ask_for_agent_roles(self, task: Task) -> List[str]:
        return self.agent.ask(PromptFactory.choose_agent(task))

    def ask_to_choose_action(self, task: Task) -> Dict[str, str]:
        action_key, reason = self.agent.ask(PromptFactory.choose_action(task))
        return {"action_name": action_key, "reason": reason}

    def ask_to_create_plan(self, task: Task, role: str) -> List[str]:
        return self.agent.ask(PromptFactory.create_plan(task, role))
