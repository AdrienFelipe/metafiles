from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Optional
from task import Task
import yaml
from prompts.prompt_strategy import IPromptStrategy


class Prompt:
    def __init__(self, task: Task, strategy: IPromptStrategy):
        self.task = task
        self.strategy = strategy

        self.env = Environment(loader=FileSystemLoader("/app/prompts/templates"))
        self.template = self.env.get_template(self.strategy.get_template_name())
        self.parsed_content = yaml.safe_load(self._render_template())

    def _render_template(self) -> str:
        render_args = self.strategy.get_render_args(self.task)
        return self.template.render(**render_args)

    def messages(self) -> List[Dict[str, str]]:
        return self.parsed_content.get("messages", [])

    def functions(self) -> Optional[List[Dict[str, Dict]]]:
        yaml_functions = self.parsed_content.get("functions", [])

        if not yaml_functions:
            return []

        functions = []
        for func in yaml_functions:
            function_dict = {
                "name": func["name"],
                "description": func["description"],
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": func["required"],
                },
            }

            for param in func["parameters"]:  # Now we iterate over the list
                if "name" in param and "type" in param:
                    param_name = param["name"]
                    function_dict["parameters"]["properties"][param_name] = {
                        "type": param["type"],
                        "description": param["description"],
                    }
                    if "enum" in param:
                        function_dict["parameters"]["properties"][param_name]["enum"] = param[
                            "enum"
                        ]
                else:
                    print(f"Unexpected parameter format: {param}")

            functions.append(function_dict)

        return functions

    def function_names(self) -> List[str]:
        return [func["name"] for func in self.functions()]

    def callback(self) -> Optional[str]:
        return self.parsed_content.get("callback", None)
