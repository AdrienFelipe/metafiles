from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from prompt.callbacks.validate_response import ValidateResponse
from prompt.commands.ask_agent_command import AskAgentCommand
from prompt.prompt_result import PostponeResponse
from task.task import Task

MAX_ITERATIONS = 5


class AskAgent(Action):
    description = "Ask a specialized agent to respond to the task by text"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        iteration = 0
        agent_proxy = AgentProxy(agent)
        roles = agent_proxy.ask_for_agent_roles(task, reason).get_roles()

        while iteration < MAX_ITERATIONS:
            validated = True
            for role in roles:
                response = AskAgentCommand(agent, task).ask(role)

                if isinstance(response, PostponeResponse):
                    return ActionResult(ActionResultStatus.PENDING, response.get_message())

                validated = validated and isinstance(response, ValidateResponse)
                task.response = response.get_message()

            if validated or len(roles) == 1:
                return ActionResult(ActionResultStatus.COMPLETED, task.response)

            iteration += 1

        return ActionResult(ActionResultStatus.FAILURE, "Max iterations reached")


action_registry.register_action(ActionName.ASK_AGENT, AskAgent)
