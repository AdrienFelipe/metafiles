from dotenv import load_dotenv

from action.action_registry import action_registry
from agent.agents.openai_agent import OpenAIAgent
from task import Task
from task_execute import execute_task


def main() -> None:
    load_dotenv()
    action_registry.register_actions()

    agent = OpenAIAgent()
    task = Task.from_yaml("/data/file_index.yaml")
    execute_task(agent, task)


if __name__ == "__main__":
    main()
