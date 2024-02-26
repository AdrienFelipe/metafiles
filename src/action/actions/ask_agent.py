from action.action import Action
from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from prompt.callbacks.validate_response import ValidateResponse
from prompt.commands.ask_agent_command import AskAgentCommand
from prompt.prompt_result import PostponeResponse
from task.task import Task

MAX_ITERATIONS = 5


class AskAgent(Action):
    action_name = ActionName.ASK_AGENT
    description = "Ask a specialized agent to respond to the task by text"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        iteration = 0
        agent_proxy = AgentProxy(self._container, agent)
        roles = agent_proxy.ask_for_agent_roles(task, reason).get_roles()
        agent_command = AskAgentCommand(self._container, agent, task)

        while iteration < MAX_ITERATIONS:
            response = agent_command.ask(roles)
            task.response = response.get_message()

            if isinstance(response, PostponeResponse):
                return ActionResult(ActionResultStatus.PENDING, task.response)

            if isinstance(response, ValidateResponse):
                return ActionResult(ActionResultStatus.COMPLETED, task.response)

            iteration += 1

        return ActionResult(ActionResultStatus.FAILURE, "Max iterations reached")
