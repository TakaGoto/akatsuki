"""Tests for CLI agent building logic."""

from my_ai_team.cli import build_agent_with_overrides, build_custom_squad, AGENTS


def test_build_agent_with_no_overrides():
    config = {"context": "", "agents": {}}
    agent = build_agent_with_overrides("kisame", config)
    assert agent.name == "Kisame"


def test_build_agent_with_yaml_context():
    config = {"context": "Stack: Next.js, Supabase.", "agents": {}}
    agent = build_agent_with_overrides("kisame", config)
    assert "Next.js" in agent.instructions


def test_build_agent_with_yaml_overrides():
    config = {
        "context": "",
        "agents": {
            "hidan": {"model": "claude-sonnet-4-5-20250929", "extra": "Check RLS."},
        },
    }
    agent = build_agent_with_overrides("hidan", config)
    assert agent.model == "claude-sonnet-4-5-20250929"
    assert "RLS" in agent.instructions


def test_build_agent_with_cli_context():
    config = {"context": "Base context.", "agents": {}}
    agent = build_agent_with_overrides("itachi", config, cli_context="Also check perf.")
    assert "Base context" in agent.instructions
    assert "Also check perf" in agent.instructions


def test_build_custom_squad():
    config = {"context": "My project.", "agents": {}}
    team = build_custom_squad(["kisame", "itachi"], config)
    assert team.name == "Pain"
    assert len(team.handoffs) == 2
    member_names = {h.name for h in team.handoffs}
    assert member_names == {"Kisame", "Itachi"}


def test_build_custom_squad_applies_overrides():
    config = {
        "context": "",
        "agents": {
            "hidan": {"extra": "Focus on auth."},
        },
    }
    team = build_custom_squad(["kisame", "hidan"], config)
    hidan = next(h for h in team.handoffs if h.name == "Hidan")
    assert "Focus on auth" in hidan.instructions
