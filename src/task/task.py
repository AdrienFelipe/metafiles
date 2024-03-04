from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

import yaml

from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from task.value_objects.user_query import UserQuery

DEFAULT_WORKDIR = "/workdir"


class Task:
    result: ActionResult = ActionResult(ActionResultStatus.PENDING, "Task not executed yet")

    def __init__(
        self,
        goal: str,
        definition: str = "",
        specifics: str = "",
        parent: Optional[Task] = None,
        plan: Optional[List[str]] = None,
        action: Optional[ActionName] = None,
        depends_on: Optional[Dict[str, Task]] = None,
        workdir: Optional[str] = None,
    ):
        self.id = Task._build_id(parent)
        self.goal = goal.strip()
        self.definition = definition.strip()
        self.specifics = specifics.strip()
        self.plan = plan or []
        self.code: str = ""
        self.response: str = ""
        self.queries: List[UserQuery] = []
        self.action = action
        self.parent = parent
        self.children: List[Task] = []
        self.index: Dict[str, Task] = {} if parent is None else parent.index
        self.index[self.id] = self
        self.depends_on: Dict[str, Task] = depends_on or {}
        self.context: Dict[str, Union[str, Callable[..., Any]]] = (
            {} if parent is None else parent.context
        )
        self.workdir: str = workdir or parent.workdir if parent else DEFAULT_WORKDIR

        if parent is not None:
            self.add_relation(parent)

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
            definition=Task.__get_as_string(data, "definition"),
            specifics=Task.__get_as_string(data, "specifics"),
            plan=data.get("plan", None),
            action=action,
        )

    @staticmethod
    def to_plan_step(
        goal: str,
        definition: List[str],
        specifics: Optional[List[str]] = None,
        depends_on: Optional[List[str]] = None,
    ) -> str:
        step = {"goal": goal, "definition": definition}
        if specifics is not None:
            step["specifics"] = specifics
        if depends_on is not None:
            step["depends_on"] = depends_on

        return yaml.dump(step, sort_keys=False, width=999).strip()

    @staticmethod
    def from_plan_step(step: str, parent_task: Optional[Task] = None) -> Task:
        data = yaml.safe_load(step)
        task = Task(
            goal=data["goal"],
            definition=Task.__get_as_string(data, "definition"),
            specifics=Task.__get_as_string(data, "specifics"),
            parent=parent_task,
        )

        # In a plan step, dependencies are expected to be relative to sibling index positions
        depends_on = data.get("depends_on", None)
        if depends_on is not None:
            dependencies = [dep for dep in task.get_siblings_by_position(depends_on)]
            task.add_dependencies(dependencies)

        return task

    @staticmethod
    def __get_as_string(data: Dict[str, Any], key: str) -> str:
        value = data.get(key, "")

        if isinstance(value, list):
            value = "\n".join(str(item) for item in value)
        elif value is None:
            value = "None"
        elif not isinstance(value, str):
            value = str(value)

        return value

    @staticmethod
    def _build_id(parent: Optional[Task]) -> str:
        if parent is None:
            return "0"

        return f"{parent.id}.{len(parent.children)}"

    def root(self) -> Task:
        if self.parent is None:
            return self

        return self.index["0"]

    def add_relation(self, parent: Task) -> None:
        parent.children.append(self)
        self.parent = parent

    def siblings(self) -> List[Task]:
        if self.parent is None:
            return [self]

        return self.parent.children

    def get_siblings_by_position(self, positions: Optional[List[int]] = None) -> List[Task]:
        if self.parent is None:
            return []

        if positions is not None:
            return [
                self.parent.children[position]
                for position in positions
                if 0 <= position < len(self.parent.children)
            ]

        return [task for task in self.parent.children if task.id != self.id]

    def get_tasks_by_ids(self, ids: List[str]) -> List[Task]:
        return [self.index[task_id] for task_id in ids if self.index.get(task_id)]

    def add_dependencies(self, tasks: List[Task]) -> None:
        for task in tasks:
            self.depends_on[task.id] = task

    def get_content(self) -> str:
        if self.action is ActionName.RUN_CODE:
            return self.code

        if self.action is ActionName.DIVIDE_TASK:
            return "\n".join(self.plan)

        return self.response
