import pytest
from core.task import Task

def test_task_creation():
    task = Task("task-001", "Test the system", priority=1)
    assert task.task_id == "task-001"
    assert task.description == "Test the system"
    assert task.priority == 1
    assert task.status == "pending"

def test_task_add_requirement():
    task = Task("task-001", "Test the system")
    task.add_requirement("Python 3.8+")
    assert "Python 3.8+" in task.requirements

def test_task_add_dependency():
    task = Task("task-001", "Test the system")
    task.add_dependency("task-002")
    assert "task-002" in task.dependencies