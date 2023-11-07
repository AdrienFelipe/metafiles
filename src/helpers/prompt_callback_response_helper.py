from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from task.task import Task

DEFAULT_PLAN: List[Dict[str, Any]] = [
    {"goal": "Setup", "specifications": ["Install X", "Configure Y"]},
    {"goal": "Test", "specifications": ["Run Z"], "depends_on": [0, 1]},
]


class PromptCallbackResponseHelper:
    def __init__(self):
        self.arguments = {}

    @staticmethod
    def simple() -> Dict[str, str]:
        return {
            "plan": '[{"goal": "Setup", "specifications": ["Install X", "Configure Y"], "depends_on": [0, 1]}]',
        }

    def get_plan(self) -> List[str]:
        return [
            Task.step_to_string(step["goal"], step["specifications"], step.get("depends_on"))
            for step in DEFAULT_PLAN
        ]

    def with_plan(
        self, plan: Optional[List[Dict[str, str]]] = None
    ) -> PromptCallbackResponseHelper:
        self.arguments["plan"] = json.dumps(plan if plan is not None else DEFAULT_PLAN)
        return self
