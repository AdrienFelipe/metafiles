from dotenv import load_dotenv

from action_registry import action_registry
from task import Task
from task_execute import execute_task


def main() -> None:
    load_dotenv()
    action_registry.register_actions()

    task = Task.from_yaml("/data/file_index.yaml")
    execute_task(task)


if __name__ == "__main__":
    main()
