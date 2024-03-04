from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from task.task import Task


class UserQuery(NamedTuple):
    question: str
    answer: str

    @staticmethod
    def add(task: Task, question: str, answer: str) -> None:
        task.queries.append(UserQuery(question, answer))
