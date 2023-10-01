# prompt.py

class Prompt:
    def __init__(self, task, step, available_actions):
        self.task = task
        self.step = step
        self.available_actions = available_actions

    def generate_messages(self):
        system_message_content = "Choose one of the available actions you'll be provided"
        user_message_content = "Available actions are:\n" + "\n".join(f"- {desc}" for desc in self.available_actions.values())
        
        return [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": user_message_content}
        ]
