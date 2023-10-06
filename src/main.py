from dotenv import load_dotenv
from registry import action_registry
from openai_chat import OpenAIChat
from prompts.prompt import Prompt
import json
from task import Task

# Constants
APPLY_ACTION = 'apply_action'
AVAILABLE_ACTIONS = {
    "1": "Ask a specialized agent to address a question or task",
    "2": "Ask the user for clarification about their goal",
    "3": "Execute an atomic code function",
    "4": "Subdivide the task into smaller tasks"
}

def apply_action(action_id, reason: str):
    print('action_id: ', action_id)
    print('reason: ', reason)

def handle_response(response):
    message = response.choices[0].message
    if message.get('function_call'):
        function_name = message['function_call']['name']
        function_arguments = json.loads(message['function_call']['arguments'])
        
        # Using a simple action handler approach
        action_handlers = {
            APPLY_ACTION: apply_action
        }
        handler = action_handlers.get(function_name)
        if handler:
            handler(**function_arguments)
        else:
            print('Agent chose a non defined function: ', function_name)
    else:
        print(message['content'])

def apply_task(task: Task) -> None:
    openai_chat = OpenAIChat()
    prompt = Prompt(task, AVAILABLE_ACTIONS)
    
    response = openai_chat.create_chat_completion(
        messages=prompt.generate_messages(),
        functions=prompt.extract_functions(),
        function_call={"name": APPLY_ACTION}
    )
    
    handle_response(response)

def main() -> None:
    load_dotenv()
    action_registry.register_actions()
    
    task = Task.from_yaml('/data/file_index.yaml')
    apply_task(task)

if __name__ == "__main__":
    main()
