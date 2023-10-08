from action import Action
from action_result import ActionResult
from agent_proxy import AgentProxy
from registry import action_registry
from task import Task


class AskAgent(Action):
    description = "Ask a specialized agent to address a question or task"

    def execute(self, task: Task, agent_proxy: AgentProxy, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""


action_registry.register_action("ask_agent", AskAgent)
