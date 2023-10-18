from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task import Task


def execute_task(agent: AgentInterface, task: Task) -> ActionResult:
    agent_proxy = AgentProxy(agent)

    if task.action:
        action_name, reason = task.action, ""
    else:
        action_name, reason = agent_proxy.ask_to_choose_action(task)

    # Now with task type, execute it's action
    action_registry.get_action(action_name).execute(agent, task, reason)
    # TODO: check task result status (success, pending, error, ...)

    # TODO: is goal complete?
    task.add_to_parent()

    return ActionResult(ActionResultStatus.PENDING)
