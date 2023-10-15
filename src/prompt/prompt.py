from typing import Any, Dict, List, Optional, Union

import yaml
from jinja2 import Environment, FileSystemLoader

from prompt.prompt_strategy import IPromptStrategy
from task import Task


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

    def add_message(self, role: str, message: str):
        if "messages" not in self.parsed_content:
            self.parsed_content["messages"] = []
        self.parsed_content["messages"].append({"role": role, "content": message})

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
                "parameters": {  # initialize an empty parameters dictionary
                    "type": "object",
                    "properties": {},
                    "required": func.get(
                        "required", []
                    ),  # using get in case 'required' is also optional
                },
            }

            # Only iterate and populate if parameters are provided
            for param in func.get("parameters", []):  # Now we iterate over the list
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

    def function_names(self) -> List[dict[Any, Any]]:
        functions = self.functions()
        if functions is None:
            return []

        return [func["name"] for func in functions]

    def callback(self) -> Union[Dict[Any, Any], str]:
        callback_name = self.parsed_content.get("callback")
        return {"name": callback_name} if callback_name else "auto"