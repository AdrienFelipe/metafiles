from __future__ import annotations

from typing import List, Optional

import yaml

from action.action_name import ActionName
from action.action_result import ActionResult


class Task:
    result: Optional[ActionResult] = None

    def __init__(
        self,
        goal: str,
        requirements: str = "",
        parent_task: Optional[Task] = None,
        plan: List[str] = [],
        action: Optional[ActionName] = None,
        tasks: List[Task] = [],
    ):
        self.id = Task.__build_id(parent_task)
        self.goal = goal
        self.requirements = requirements
        self.parent_task = parent_task
        self.plan = plan
        self.action = action
        self.tasks = tasks

    @staticmethod
    def from_yaml(file_path: str, parent_task: Optional[Task] = None) -> Task:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        try:
            action_name = data.get("action", None)
            action = ActionName(action_name) if action_name else None
        except ValueError:
            print(f"Loaded task with invalid action name (file: {file_path}, action: {action_name}")
            action = None

        return Task(
            goal=data["goal"],
            requirements=data["requirements"],
            parent_task=parent_task,
            plan=data.get("plan", None),
            action=action,
        )

    def __str__(self) -> str:
        return f"Goal: {self.goal}, Requirements: {self.requirements}, Plan: {', '.join(self.plan)}"

    @staticmethod
    def __build_id(parent_task: Optional[Task]) -> str:
        if parent_task is None:
            return "0"

        return f"{parent_task.id}.{len(parent_task.plan)}"

    def add_to_parent(self) -> None:
        if self.parent_task is not None:
            self.parent_task.tasks.append(self)

    def get_parent_tasks(self) -> List[Task]:
        if self.parent_task is None or self.parent_task.tasks is None:
            return []

        return self.parent_task.tasks
