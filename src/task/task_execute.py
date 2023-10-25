from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task.task import Task


def execute_task(agent: AgentInterface, task: Task) -> None:
    agent_proxy = AgentProxy(agent)

    if task.action:
        action_name, reason = task.action, ""
    else:
        response = agent_proxy.ask_to_choose_action(task)
        action_name, reason = response.get_action_name(), response.get_reason()

    # TODO: validate action is valid (not NO_ACTION)

    # Now with task type, execute it's action
    task.result = action_registry.get_action(action_name).execute(agent, task, reason)
    # TODO: check task result status (success, pending, error, ...)

    # TODO: is goal complete?
    task.add_to_parent()
