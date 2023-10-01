import yaml
from dotenv import load_dotenv
from registry import action_registry
from openai_chat import OpenAIChat
from prompts.prompt import Prompt


def orchestrate_conversation(task, step):
    print(f"Executing task: {task} under step: {step}")
    
    # Initialize OpenAI Chat and Prompt classes
    openai_chat = OpenAIChat()
    
    available_actions = action_registry.get_registered_actions()
    prompt = Prompt(task, step, available_actions)
    messages = prompt.generate_messages()
    
    response = openai_chat.create_chat_completion(messages=messages)

    # Handle the response as necessary
    print(response.choices[0].message['content'])


def execute_goal(goal):
    context = goal['context']
    print(f"Goal: {goal['name']}")
    print(f"Context: {context}")
    
    for step in goal['steps']:
        step_name = step['name']
        for task in step['tasks']:
            orchestrate_conversation(task, step_name)


def main():
    load_dotenv()
    action_registry.register_actions()
    
    with open('/data/steps.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    execute_goal(data['goal'])


if __name__ == "__main__":
    main()
