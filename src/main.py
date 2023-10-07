from dotenv import load_dotenv
from registry import action_registry
from openai_chat import OpenAIChat
from task import Task
from prompts.prompt_factory import PromptFactory


def apply_task(task: Task) -> None:
    # If no task type, generate task type
    prompt = PromptFactory.choose_action(task)

    agent = OpenAIChat()
    result = agent.ask(prompt)

    # Now with task type, execute it's action
    # check task result status (success, pending, error, ...)
    # maybe re-loop


def main() -> None:
    load_dotenv()
    action_registry.register_actions()

    task = Task.from_yaml("/data/file_index.yaml")
    apply_task(task)


if __name__ == "__main__":
    main()
