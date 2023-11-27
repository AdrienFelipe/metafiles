from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from task.task import Task


class AskUser(Action):
    description = "Request additional information from the user"

    def execute(self, agent: AgentInterface, task: Task, query: str = "") -> ActionResult:
        input = self.query_user(query)
        return ActionResult(ActionResultStatus.SUCCESS, input)

    def query_user(self, query: str) -> str:
        return input(f"Please clarify: {query}\n")


action_registry.register_action(ActionName.ASK_USER, AskUser)
