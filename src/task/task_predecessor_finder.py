from typing import List, Optional

from task.task import Task


class TaskPredecessorFinder:
    @staticmethod
    def generate(task: Task) -> List[Task]:
        return TaskPredecessorFinder._collect_previous_tasks(task)

    @staticmethod
    def _collect_previous_tasks(
        task: Task, collected_tasks: Optional[List[Task]] = None
    ) -> List[Task]:
        if collected_tasks is None:
            collected_tasks = []

        # Use list comprehension and next() to find the index of the current task
        siblings = task.siblings()
        current_task_index = next(
            (i for i, sibling in enumerate(siblings) if sibling.id == task.id), None
        )

        if current_task_index is not None:
            # Extend the collected tasks with siblings before the current task
            collected_tasks[0:0] = siblings[:current_task_index]

        # Recursively collect from parent task, if it exists
        if task.parent:
            return TaskPredecessorFinder._collect_previous_tasks(task.parent, collected_tasks)

        return collected_tasks


# Usage example:
# task = <some Task object>
# previous_tasks = PreviousTasksListGenerator.generate_previous_tasks_list(task)
# for task in previous_tasks:
#     # Do something with each task
