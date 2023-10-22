from dotenv import load_dotenv

from action.action_registry import action_registry
from agent.agents.openai_agent import OpenAIAgent
from task.task import Task
from task.task_execute import execute_task


def bootstrap() -> None:
    load_dotenv()
    action_registry.register_actions()


def main() -> None:
    bootstrap()

    agent = OpenAIAgent()
    task = Task.from_yaml("/data/file_index.yaml")
    execute_task(agent, task)


if __name__ == "__main__":
    main()
