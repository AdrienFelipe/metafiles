from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task.task import Task


class AskAgent(Action):
    description = "Deploy a specialized agent to handle a query or task"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        """Apply the action given a task and a reason."""
        agent_proxy = AgentProxy(agent)
        return ActionResult(ActionResultStatus.PENDING)


action_registry.register_action(ActionName.ASK_AGENT, AskAgent)
