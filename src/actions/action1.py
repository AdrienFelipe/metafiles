# actions/action1.py

from registry import action_registry

class Action1:
    description = "This is Action1"

action_registry.register_action('action1', Action1)
