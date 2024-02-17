from action.action import Action
from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from task.task import Task


class AskUser(Action):
    action_name = ActionName.ASK_USER
    description = "Request additional information from the user (don't use it for now)"

    def execute(self, agent: AgentInterface, task: Task, query: str = "") -> ActionResult:
        input = self.query_user(query)
        return ActionResult(ActionResultStatus.COMPLETED, input)

    def query_user(self, query: str) -> str:
        return input(f"Please clarify: {query}\n")
