from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from task.task import Task

DEFAULT_PLAN: List[Dict[str, Any]] = [
    {"goal": "Setup", "definition": ["Install X", "Configure Y"], "specifics": ["Run A"]},
    {"goal": "Test", "definition": ["Run Z"], "depends_on": [0, 1]},
]

DEFAULT_CODE: str = "var = 'ok'\nprint(var)"


class PromptCallbackResponseHelper:
    def __init__(self):
        self.arguments = {}

    @staticmethod
    def simple() -> Dict[str, str]:
        return {
            "plan": '[{"goal": "Setup", "definition": ["Install X","Configure Y"], "specifics": ["Run A"], "depends_on": [0, 1]}]',
            "code": "var = 'ok'\nprint(var)",
        }

    def get_plan(self) -> List[str]:
        return [
            Task.to_plan_step(
                goal=step["goal"],
                definition=step["definition"],
                specifics=step.get("specifics"),
                depends_on=step.get("depends_on"),
            )
            for step in DEFAULT_PLAN
        ]

    def with_plan(
        self, plan: Optional[List[Dict[str, str]]] = None
    ) -> PromptCallbackResponseHelper:
        self.arguments["plan"] = json.dumps(plan if plan is not None else DEFAULT_PLAN)
        return self

    def get_code(self) -> str:
        return self.arguments["code"]

    def with_code(self, code: Optional[str] = None) -> PromptCallbackResponseHelper:
        self.arguments["code"] = code if code is not None else DEFAULT_CODE
        return self
