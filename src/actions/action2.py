# actions/action2.py

from registry import action_registry

class Action2:
    description = "This is Action2"

action_registry.register_action('action2', Action2)
