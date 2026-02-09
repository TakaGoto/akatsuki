"""Basic tests for agent creation."""

from my_ai_team import create_agent, create_team
from my_ai_team.agents.presets import researcher, coder, reviewer, writer


def test_create_agent():
    agent = create_agent(name="Test", instructions="You are a test agent.")
    assert agent.name == "Test"


def test_create_team():
    member = create_agent(name="Worker", instructions="You do work.")
    lead = create_team(name="Lead", instructions="You lead.", members=[member])
    assert lead.name == "Lead"
    assert len(lead.handoffs) == 1


def test_preset_researcher():
    agent = researcher()
    assert agent.name == "Researcher"


def test_preset_coder():
    agent = coder()
    assert agent.name == "Coder"


def test_preset_reviewer():
    agent = reviewer()
    assert agent.name == "Reviewer"


def test_preset_writer():
    agent = writer()
    assert agent.name == "Writer"


def test_preset_with_extra_instructions():
    agent = coder(extra_instructions="Use Python 3.12 features.")
    assert "Python 3.12" in agent.instructions
