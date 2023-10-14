import importlib
import os
from typing import Dict

from action.action import Action, ActionName

ACTIONS_DIR = "/app/actions"


class ActionRegistry:
    _actions: Dict[ActionName, Action] = {}

    def register_action(self, name: ActionName, action_class):
        self._actions[name] = action_class()

    def get_action(self, name: ActionName) -> Action:
        return self._actions[name]

    def get_registered_actions(self):
        return {name: action.description for name, action in self._actions.items()}

    def register_actions(self):
        for filename in os.listdir(ACTIONS_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove '.py' extension
                importlib.import_module(f"actions.{module_name}")


# Create an instance of the ActionRegistry class
action_registry = ActionRegistry()
