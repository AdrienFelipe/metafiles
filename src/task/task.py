from __future__ import annotations

from typing import Dict, List, Optional

import yaml

from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus


class Task:
    result: ActionResult = ActionResult(ActionResultStatus.PENDING, "Task not executed yet")

    def __init__(
        self,
        goal: str,
        requirements: str = "",
        parent: Optional[Task] = None,
        plan: Optional[List[str]] = None,
        action: Optional[ActionName] = None,
        depends_on: Optional[List[str]] = None,
    ):
        self.id = Task._build_id(parent)
        self.goal = goal
        self.requirements = requirements
        self.plan = plan or []
        self.action = action
        self.parent = parent
        self.children: List[Task] = []
        self.index: Dict[str, Task] = {} if parent is None else parent.index
        self.depends_on = depends_on or []

        self.add_to_parent()

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
            parent=parent_task,
            plan=data.get("plan", None),
            action=action,
        )

    @staticmethod
    def step_to_string(
        goal: str, specifications: List[str], depends_on: Optional[List[str]] = None
    ) -> str:
        step = {"goal": goal, "specifications": specifications}
        if depends_on is not None:
            step["depends_on"] = depends_on

        return yaml.dump(step, sort_keys=False, width=999).strip()

    @staticmethod
    def from_string(step: str, parent_task: Optional[Task] = None) -> Task:
        data = yaml.safe_load(step)
        if parent_task is not None:
            data["depends_on"] = [
                task.id for task in parent_task.get_tasks_by_ids(data["depends_on"])
            ]

        return Task(
            goal=data["goal"],
            requirements=data["specifications"],
            parent=parent_task,
        )

    def __str__(self) -> str:
        return f"Goal: {self.goal}, Requirements: {self.requirements}, Plan: {', '.join(self.plan)}"

    @staticmethod
    def _build_id(parent: Optional[Task]) -> str:
        if parent is None:
            return "0"

        return f"{parent.id}.{len(parent.children)}"

    def add_to_parent(self) -> None:
        if self.parent is not None:
            self.parent.children.append(self)

        self.index[self.id] = self

    def remove_from_parent(self) -> None:
        if self.parent is not None:
            self.parent.children.remove(self)
        del self.index[self.id]

    def get_siblings(self) -> List[Task]:
        return [] if self.parent is None else self.parent.children

    def get_tasks_by_ids(self, ids: List[str]) -> List[Task]:
        return [self.index[task_id] for task_id in ids if self.index.get(task_id)]
