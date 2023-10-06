from typing import Any, Dict
from task import Task
from prompts.prompt_strategy import IPromptStrategy

class ChooseAgentStrategy(IPromptStrategy):
    TEMPLATE_NAME = 'choose_agent.yaml'

    def get_template_name(self) -> str:
        return self.TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "name": task.name,
            "goal": task.goal
        }
