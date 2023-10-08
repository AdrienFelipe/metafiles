from dotenv import load_dotenv

from agent_proxy import AgentProxy
from openai_chat import OpenAIChat
from registry import action_registry
from task import Task
from task_execute import execute_task


def main() -> None:
    load_dotenv()
    action_registry.register_actions()
    agent_proxy = AgentProxy(OpenAIChat())

    task = Task.from_yaml("/data/file_index.yaml")
    execute_task(task, agent_proxy)


if __name__ == "__main__":
    main()
