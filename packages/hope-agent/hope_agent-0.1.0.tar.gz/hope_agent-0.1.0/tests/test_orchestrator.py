import pytest
from core.orchestrator import Orchestrator
from core.agent import Agent
from core.task import Task

@pytest.fixture
def orchestrator():
    return Orchestrator()

def test_add_agent(orchestrator):
    agent = Agent({"agent_id": "test-agent-001", "name": "Test Agent"})
    orchestrator.add_agent(agent)
    assert "test-agent-001" in orchestrator.agents

def test_add_task(orchestrator):
    task = Task("task-001", "Test task")
    orchestrator.add_task(task)
    assert task in orchestrator.tasks

@pytest.mark.asyncio
async def test_execute_task(orchestrator):
    agent = Agent({"agent_id": "test-agent-001", "name": "Test Agent"})
    orchestrator.add_agent(agent)
    task = Task("task-001", "Test task")
    result = await orchestrator.execute_task(task)
    assert result is not None  # Implement actual logic in Orchestrator class

def test_use_plugin(orchestrator):
    # Assuming a test plugin is registered
    result = orchestrator.use_plugin("test_plugin", "test_arg")
    assert result is not None  # Implement actual plugin system