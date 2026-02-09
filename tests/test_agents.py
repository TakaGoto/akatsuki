"""Tests for agent creation and presets."""

from my_ai_team import create_agent, create_team, dev_team, full_team
from my_ai_team.agents.presets import (
    tech_lead,
    feature_dev,
    mobile_dev,
    test_engineer,
    code_reviewer,
    security_auditor,
    bug_hunter,
    docs_writer,
    devops,
)


# -- create_agent / create_team --


def test_create_agent():
    agent = create_agent(name="Test", instructions="You are a test agent.")
    assert agent.name == "Test"


def test_create_team():
    member = create_agent(name="Worker", instructions="You do work.")
    lead = create_team(name="Lead", instructions="You lead.", members=[member])
    assert lead.name == "Lead"
    assert len(lead.handoffs) == 1


# -- Individual presets --


def test_tech_lead():
    agent = tech_lead()
    assert agent.name == "Tech Lead"
    assert "coordinating" in agent.instructions


def test_feature_dev():
    agent = feature_dev()
    assert agent.name == "Feature Dev"
    assert "minimal and focused" in agent.instructions


def test_mobile_dev():
    agent = mobile_dev()
    assert agent.name == "Mobile Dev"
    assert "React Native" in agent.instructions


def test_test_engineer():
    agent = test_engineer()
    assert agent.name == "Test Engineer"
    assert "AAA pattern" in agent.instructions


def test_code_reviewer():
    agent = code_reviewer()
    assert agent.name == "Code Reviewer"
    assert "READ-ONLY" in agent.instructions


def test_security_auditor():
    agent = security_auditor()
    assert agent.name == "Security Auditor"
    assert "OWASP" in agent.instructions


def test_security_auditor_uses_opus_by_default():
    agent = security_auditor()
    assert agent.model == "claude-opus-4-6"


def test_bug_hunter():
    agent = bug_hunter()
    assert agent.name == "Bug Hunter"
    assert "root cause" in agent.instructions.lower()


def test_docs_writer():
    agent = docs_writer()
    assert agent.name == "Docs Writer"
    assert "Documentation" in agent.instructions


def test_devops():
    agent = devops()
    assert agent.name == "DevOps"
    assert "CI/CD" in agent.instructions


# -- extra_instructions --


def test_extra_instructions():
    agent = feature_dev(extra_instructions="Use Python 3.12 features.")
    assert "Python 3.12" in agent.instructions


def test_security_auditor_custom_model():
    agent = security_auditor(model="claude-sonnet-4-5-20250929")
    assert agent.model == "claude-sonnet-4-5-20250929"


# -- Team presets --


def test_dev_team():
    team = dev_team()
    assert team.name == "Tech Lead"
    assert len(team.handoffs) == 4
    member_names = {h.name for h in team.handoffs}
    assert member_names == {"Feature Dev", "Test Engineer", "Code Reviewer", "Security Auditor"}


def test_full_team():
    team = full_team()
    assert team.name == "Tech Lead"
    assert len(team.handoffs) == 8
    member_names = {h.name for h in team.handoffs}
    assert "Feature Dev" in member_names
    assert "Mobile Dev" in member_names
    assert "Bug Hunter" in member_names
    assert "DevOps" in member_names


def test_dev_team_with_context():
    team = dev_team(extra_instructions="Stack: Next.js, Supabase, TypeScript")
    assert "Next.js" in team.instructions
