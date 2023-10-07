from typing import Any, Callable, Dict, Optional
from callbacks import update_plan
from task import Task
from prompts.prompt_strategy import IPromptStrategy


class CreatePlanStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_plan.yaml"
    _HANDLER_FUNCTIONS = {"update_plan": update_plan}

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {"name": task.name, "goal": task.goal}

    def get_handler_function(self, function_name: str) -> Optional[Callable]:
        return self._HANDLER_FUNCTIONS.get(function_name)
