import yaml

def orchestrate_conversation(task, step):
    print(f"Executing task: {task} under step: {step}")
    # The existing orchestrate_conversation function
    # Here, you'll implement the logic of the conversations among the agents as required.

def execute_goal(goal):
    context = goal['context']
    print(f"Goal: {goal['name']}")
    print(f"Context: {context}")
    
    for step in goal['steps']:
        step_name = step['name']
        for task in step['tasks']:
            orchestrate_conversation(task, step_name)

def main():
    with open('/data/steps.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    execute_goal(data['goal'])

if __name__ == "__main__":
    main()
