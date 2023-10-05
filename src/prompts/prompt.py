from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Optional
from task import Task
import yaml

class Prompt:
    def __init__(self, task: Task, available_actions: Dict[str, str]):
        self.task = task
        self.available_actions = available_actions

        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader('/app/prompts'))
        self.template = self.env.get_template('choose_action.yaml')
        self.rendered_content = self._render_template()

    def _render_template(self) -> str:
        return self.template.render(
            name=self.task.name, 
            goal=self.task.goal, 
            actions=self.available_actions.values()
        )

    def generate_messages(self) -> List[Dict[str, str]]:
        parsed_content = yaml.safe_load(self.rendered_content)
        return parsed_content.get("messages", [])

    def extract_functions(self) -> Optional[List[Dict[str, Dict]]]:
        rendered_content = self._render_template()
        parsed_content = yaml.safe_load(rendered_content)
        yaml_functions = parsed_content.get("functions", [])

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
                    "required": func["required"]
                }
            }

            for param in func["parameters"]:  # Now we iterate over the list
                if "name" in param and "type" in param: 
                    param_name = param["name"]
                    function_dict["parameters"]["properties"][param_name] = {
                        "type": param["type"],
                        "description": param["description"]
                    }
                    if "enum" in param:
                        function_dict["parameters"]["properties"][param_name]["enum"] = param["enum"]
                else:
                    print(f"Unexpected parameter format: {param}")

            functions.append(function_dict)

        return functions
