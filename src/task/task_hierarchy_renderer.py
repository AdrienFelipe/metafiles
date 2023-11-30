from typing import List, Optional

from task.task import Task


class TaskHierarchyRenderer:
    @staticmethod
    def render_hierarchy(task: Task, indent_size: int = 2) -> str:
        return "\n".join(TaskHierarchyRenderer._build_hierarchy(task, indent_size))

    @staticmethod
    def _build_hierarchy(
        task: Task, indent_size: int, accumulated_lines: Optional[List[str]] = None
    ) -> List[str]:
        indent_spaces = " " * indent_size
        hierarchy_lines: List[str] = []

        if accumulated_lines is None:
            accumulated_lines = []
        else:
            accumulated_lines = [f"{indent_spaces}{line}" for line in accumulated_lines]

        for sibling in task.siblings():
            task_label = f"{sibling.id} - {sibling.goal}"
            hierarchy_lines.append(task_label)
            if sibling.id == task.id:
                hierarchy_lines.extend(accumulated_lines)

        if task.parent is None:
            return hierarchy_lines

        return TaskHierarchyRenderer._build_hierarchy(task.parent, indent_size, hierarchy_lines)
