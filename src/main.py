from dotenv import load_dotenv
from registry import action_registry
from openai_chat import OpenAIChat
from prompts.prompt import Prompt
import json
from task import Task


def apply_task(task: Task) -> None:
    print(f"Executing task: {task}")
    
    # Check whether task goal can be achived from a single action,
    # or should be divided into multiple sub-tasks
    # --> prompt: this is the goal, these are the actions
    #     can a single action complete the task?
    #        return the corresponding task type 
    # Task list, create a plan for the task
    #   ie, list the first level sub-tasks to complete the task
    
    # Set task type based on previous response
    
    # If task is action, execute action
    # Else, apply plan each sub-task
    
    # Initialize OpenAI Chat and Prompt classes
    openai_chat = OpenAIChat()
    
    #available_actions = action_registry.get_registered_actions()
    available_actions = {
        "1": "Ask a specialized agent to address a question or task",
        "2": "Ask the user for clarification about their goal",
        "3": "Execute an atomic code function",
        "4": "Subdivide the task into smaller tasks"
    }

    prompt = Prompt(task, available_actions)
    messages = prompt.generate_messages()
    functions = prompt.extract_functions()
    
    response = openai_chat.create_chat_completion(messages=messages, functions=functions)
    message = response.choices[0].message
    
    # If is function call
    if message['function_call']:
        function_name = message['function_call']['name'] # expected apply_action
        function_arguments = json.loads(message['function_call']['arguments'])
        
        if function_name == 'apply_action':
            apply_action(function_arguments['action_id'], function_arguments['reason'])
    
    # Handle the response as necessary
    else:
        print(message['content'])

def apply_action(action_id, reason: str):
    print('action_id: ', action_id)
    print('reason: ', reason)

def main() -> None:
    load_dotenv()
    action_registry.register_actions()
    
    # Capture goal from user
    
    # Transform goal into a task
    task = Task.from_yaml('/data/file_index.yaml')
    apply_task(task)


if __name__ == "__main__":
    main()
