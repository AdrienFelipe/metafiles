from __future__ import annotations

import importlib
import os
from typing import Dict, Type

from action.action import Action
from action.action_name import ActionName
from action.action_registry_interface import IActionRegistry
from core.service.service_container import ServiceContainer

ACTIONS_DIR = "/app/action/actions"


class ActionRegistry(IActionRegistry):
    _actions: Dict[ActionName, Type[Action]] = {}

    def __init__(self, container: ServiceContainer):
        self._container = container

    def get_action(self, name: ActionName) -> Action:
        return self._actions[name](self._container)

    @classmethod
    def register_action(cls, name: ActionName, action_class: Type[Action]):
        cls._actions[name] = action_class

    @classmethod
    def get_registered_actions(cls):
        return {
            action_name.value: action_class.description
            for action_name, action_class in cls._actions.items()
            if action_name != ActionName.NO_ACTION
        }

    @classmethod
    def register_actions(cls):
        for filename in os.listdir(ACTIONS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove '.py' extension
                module = importlib.import_module(f"action.actions.{module_name}")
                # Dynamically discover action classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Action) and attr is not Action:
                        # Assuming the action class has a 'action_name' attribute for registration
                        cls.register_action(attr.action_name, attr)
