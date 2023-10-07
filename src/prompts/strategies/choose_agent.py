from typing import Any, Callable, Dict, Optional
from callbacks import ask_agents
from task import Task
from prompts.prompt_strategy import IPromptStrategy


class ChooseAgentStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_agent.yaml"
    _HANDLER_FUNCTIONS = {
        "ask_agents": ask_agents,
    }

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {"name": task.name, "goal": task.goal}

    def get_handler_function(self, function_name: str) -> Optional[Callable]:
        return self._HANDLER_FUNCTIONS.get(function_name)
