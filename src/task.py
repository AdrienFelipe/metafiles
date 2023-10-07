from __future__ import annotations

from typing import List

import yaml


class Task:
    def __init__(self, name: str, goal: str, plan: List[str], action: str = None):
        self.name = name
        self.goal = goal
        self.plan = plan
        self.action = action

    @staticmethod
    def from_yaml(file_path: str) -> Task:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return Task(data["name"], data["goal"], data.get("plan", None), data.get("action", None))

    def __str__(self) -> str:
        return f"Name: {self.name}, Goal: {self.goal}, Plan: {', '.join(self.plan)}"
