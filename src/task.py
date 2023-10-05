import yaml
from typing import List


class Task:
    def __init__(self, name: str, goal: str, plan: List[str]):
        self.name = name
        self.goal = goal
        self.plan = plan

    @staticmethod
    def from_yaml(file_path: str) -> 'Task':
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return Task(data['name'], data['goal'], data['plan'])

    def __str__(self) -> str:
        return f"Name: {self.name}, Goal: {self.goal}, Plan: {', '.join(self.plan)}"