from __future__ import annotations

from typing import List, Optional

import yaml


class Task:
    def __init__(
        self,
        goal: str,
        requirements: str,
        parent_task: Task = None,
        plan: List[str] = [],
        action: str = None,
    ):
        self.id = Task.__build_id(parent_task)
        self.goal = goal
        self.requirements = requirements
        self.parent_task = parent_task
        self.plan = plan
        self.action = action

    @staticmethod
    def from_yaml(file_path: str, parent_task: Task = None) -> Task:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return Task(
            data["goal"],
            data["requirements"],
            parent_task,
            data.get("plan", None),
            data.get("action", None),
        )

    def __str__(self) -> str:
        return f"Goal: {self.goal}, Requirements: {self.requirements}, Plan: {', '.join(self.plan)}"

    @staticmethod
    def __build_id(parent_task: Optional[Task]) -> str:
        if parent_task is None:
            return "0"

        return f"{parent_task.id}.{len(parent_task.plan)}"
