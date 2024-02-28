from enum import Enum

from task.task import Task


class InteractionType(Enum):
    AGENT_QUERY = "Agent Query"


class Interaction:
    def __init__(self, interaction_type: InteractionType, task: Task, message: str, status: str):
        self.type = interaction_type
        self.task = task
        self.message = message
        self.status = status

    def __repr__(self):
        return f"[Task {self.task.id}] {self.type.value}: {self.message} (Status: {self.status})"
