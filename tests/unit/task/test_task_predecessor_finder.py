from task.task import Task
from task.task_predecessor_finder import TaskPredecessorFinder


def test_no_predecessors_for_root_task():
    root_task = Task("Root Task")
    assert TaskPredecessorFinder.generate(root_task) == []


def test_single_predecessors():
    parent_task = Task("Parent Task")
    middle_task = Task("Middle Task", parent=parent_task)
    task = Task("Task 1", parent=middle_task)
    assert TaskPredecessorFinder.generate(task) == []


def test_predecessors_with_siblings():
    parent_task = Task("Parent Task")
    sibling_task = Task("Sibling Task", parent=parent_task)
    task = Task("Task 1", parent=parent_task)
    assert TaskPredecessorFinder.generate(task) == [sibling_task]


def test_three_level_hierarchy_with_siblings():
    # Level 1 (Root)
    root_task = Task("Root Task")
    level1_task = Task("Root Sibling 1", parent=root_task)
    middle_task = Task("Root Sibling 2 (Parent)", parent=root_task)
    Task("Root Sibling 3", parent=root_task)

    # Level 2
    level2_1_task = Task("Middle Sibling 1", parent=middle_task)
    level2_2_task = Task("Middle Sibling 2", parent=middle_task)
    inner_task = Task("Middle Sibling 2 (Parent)", parent=middle_task)
    Task("Middle Sibling 3", parent=middle_task)

    # Level 3 (Current Task)
    level3_task = Task("Inner Sibling 1", parent=inner_task)
    current_task = Task("Current Task", parent=inner_task)
    Task("Inner Sibling 2", parent=inner_task)

    # Expected predecessors: Siblings before the current task at each level and their parent tasks
    expected_predecessors = [level1_task, level2_1_task, level2_2_task, level3_task]
    assert TaskPredecessorFinder.generate(current_task) == expected_predecessors
