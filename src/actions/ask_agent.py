from action import Action, ActionName
from action_registry import action_registry
from action_result import ActionResult, ActionResultStatus
from agent_interface import AgentInterface
from agent_proxy import AgentProxy
from task import Task


class AskAgent(Action):
    description = "Ask a specialized agent to address a question or task"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        """Apply the action given a task and a reason."""
        agent_proxy = AgentProxy(agent)
        return ActionResult(ActionResultStatus.PENDING)


action_registry.register_action(ActionName.ASK_AGENT, AskAgent)
