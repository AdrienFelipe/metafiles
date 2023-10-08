from agent_proxy import AgentProxy
from registry import action_registry
from task import Task


def execute_task(task: Task, agent_proxy: AgentProxy) -> None:
    # If no task type, generate task type
    if task.action:
        action_key = task.action
        reason = None
    else:
        action_key, reason = agent_proxy.ask_to_choose_action(task)

    # Now with task type, execute it's action
    action_registry.get_action(action_key).execute(task, agent_proxy, reason)
    # TODO: check task result status (success, pending, error, ...)

    # TODO: is goal complete?
