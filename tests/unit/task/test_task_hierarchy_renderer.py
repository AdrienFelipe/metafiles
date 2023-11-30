from task.task import Task
from task.task_hierarchy_renderer import TaskHierarchyRenderer


def test_single_task_without_parent():
    task = Task("Task 1")
    expected_output = "0 - Task 1"
    assert TaskHierarchyRenderer.render_hierarchy(task) == expected_output


def test_single_task_with_parent():
    parent_task = Task("Parent Task")
    task = Task("Task 1", parent=parent_task)
    expected_output = "0 - Parent Task\n  0.0 - Task 1"
    assert TaskHierarchyRenderer.render_hierarchy(task) == expected_output


def test_task_with_siblings():
    parent_task = Task("Root Task")
    Task("Task 1", parent=parent_task)
    task = Task("Task 2", parent=parent_task)
    expected_output = "0 - Root Task\n  0.0 - Task 1\n  0.1 - Task 2"
    assert TaskHierarchyRenderer.render_hierarchy(task) == expected_output


def test_task_hierarchy_with_multiple_levels():
    grandparent_task = Task("Grandparent Task")
    parent_task = Task("Parent Task", parent=grandparent_task)
    task = Task("Task 1", parent=parent_task)
    expected_output = "0 - Grandparent Task\n  0.0 - Parent Task\n    0.0.0 - Task 1"
    assert TaskHierarchyRenderer.render_hierarchy(task) == expected_output


def test_custom_indentation_size():
    parent_task = Task("Parent Task")
    task = Task("Task 1", parent=parent_task)
    expected_output = "0 - Parent Task\n    0.0 - Task 1"  # 4 spaces indentation
    assert TaskHierarchyRenderer.render_hierarchy(task, indent_size=4) == expected_output


def test_task_without_children():
    parent_task = Task("Parent Task")
    Task("Task 1", parent=parent_task)
    expected_output = "0 - Parent Task"
    assert TaskHierarchyRenderer.render_hierarchy(parent_task) == expected_output
