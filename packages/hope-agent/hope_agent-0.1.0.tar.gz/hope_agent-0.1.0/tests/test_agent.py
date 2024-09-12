import pytest
from core.agent import Agent

@pytest.fixture
def sample_agent_data():
    return {
        "agent_id": "test-agent-001",
        "name": "Test Agent",
        "role": "Tester",
        "attributes": {
            "intelligence": 0.8,
            "creativity": 0.7,
            "efficiency": 0.9,
            "empathy": 0.6
        },
        "skills": [
            {"name": "Testing", "proficiency": 0.9},
            {"name": "Debugging", "proficiency": 0.8}
        ],
        "main_task": "Perform various tests on the system"
    }

def test_agent_creation(sample_agent_data):
    agent = Agent(sample_agent_data)
    assert agent.agent_id == "test-agent-001"
    assert agent.name == "Test Agent"
    assert agent.role == "Tester"
    assert agent.attributes["intelligence"] == 0.8
    assert len(agent.skills) == 2
    assert agent.main_task == "Perform various tests on the system"

def test_agent_process_task():
    agent = Agent({"agent_id": "test-agent-001", "name": "Test Agent"})
    task = {"description": "Run unit tests"}
    result = agent.process_task(task)
    assert result is not None  # Implement actual logic in Agent class