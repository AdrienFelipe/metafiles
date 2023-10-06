from dotenv import load_dotenv
from registry import action_registry
from openai_chat import OpenAIChat
import json
from action_result import ActionResult
from task import Task
from prompts.prompt_factory import PromptFactory

# Constants
APPLY_ACTION = "apply_action"


def apply_task(task: Task) -> None:
    # If no task type, generate task type
    openai_chat = OpenAIChat()
    prompt = PromptFactory.choose_action(task)

    response = openai_chat.create_chat_completion(
        messages=prompt.generate_messages(),
        functions=prompt.extract_functions(),
        function_call={"name": APPLY_ACTION},
    )

    # Now with task type, execute it's action
    result = handle_response(task, response)

    # check task result status (success, pending, error, ...)
    # maybe re-loop


def handle_response(task: Task, response):
    message = response.choices[0].message
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_arguments = json.loads(message["function_call"]["arguments"])

        # Using a simple action handler approach
        action_handlers = {APPLY_ACTION: apply_action}
        handler = action_handlers.get(function_name)
        if handler:
            handler(task, **function_arguments)
        else:
            print("Agent chose a non defined function: ", function_name)
    else:
        print(message["content"])


def apply_action(task: Task, action_key: str, reason: str) -> ActionResult:
    print("Apply action", action_key, reason)
    return action_registry.get_action(action_key).apply(task, reason)


def main() -> None:
    load_dotenv()
    action_registry.register_actions()

    task = Task.from_yaml("/data/file_index.yaml")
    apply_task(task)


if __name__ == "__main__":
    main()
