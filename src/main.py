from dotenv import load_dotenv

from agent_proxy import AgentProxy
from openai_chat import OpenAIChat
from registry import action_registry
from task import Task


def apply_task(task: Task) -> None:
    # If no task type, generate task type
    if task.action:
        action_key = task.action
        reason = None
    else:
        agent_proxy = AgentProxy(OpenAIChat())
        action_key, reason = agent_proxy.ask_to_choose_action(task)

    # Now with task type, execute it's action
    action_registry.get_action(action_key).execute(task, reason)
    # check task result status (success, pending, error, ...)
    # maybe re-loop


def main() -> None:
    load_dotenv()
    action_registry.register_actions()

    task = Task.from_yaml("/data/file_index.yaml")
    apply_task(task)


if __name__ == "__main__":
    main()
