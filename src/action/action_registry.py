import importlib
import os
from typing import Dict, Type

from action.action import Action
from action.action_name import ActionName

ACTIONS_DIR = "/app/action/actions"


class ActionRegistry:
    _actions: Dict[ActionName, Action] = {}

    def register_action(self, name: ActionName, action_class: Type[Action]):
        self._actions[name] = action_class()

    def get_action(self, name: ActionName) -> Action:
        return self._actions[name]

    def get_registered_actions(self):
        return {name.value: action.description for name, action in self._actions.items()}

    def register_actions(self):
        for filename in os.listdir(ACTIONS_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove '.py' extension
                importlib.import_module(f"action.actions.{module_name}")


# Create an instance of the ActionRegistry class
action_registry = ActionRegistry()
