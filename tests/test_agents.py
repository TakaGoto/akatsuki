"""Tests for Akatsuki agent presets and teams."""

from my_ai_team import dev_team, full_team
from my_ai_team.agents.presets import (
    pain,
    kisame,
    tobi,
    sasori,
    itachi,
    hidan,
    deidara,
    konan,
    kakuzu,
)


# -- Individual agents --


def test_pain():
    agent = pain()
    assert agent.name == "Pain"
    assert "coordinate" in agent.instructions.lower()


def test_kisame():
    agent = kisame()
    assert agent.name == "Kisame"
    assert "Feature Development" in agent.instructions


def test_tobi():
    agent = tobi()
    assert agent.name == "Tobi"
    assert "React Native" in agent.instructions


def test_sasori():
    agent = sasori()
    assert agent.name == "Sasori"
    assert "AAA pattern" in agent.instructions


def test_itachi():
    agent = itachi()
    assert agent.name == "Itachi"
    assert "READ-ONLY" in agent.instructions


def test_hidan():
    agent = hidan()
    assert agent.name == "Hidan"
    assert "OWASP" in agent.instructions


def test_hidan_uses_opus_by_default():
    agent = hidan()
    assert agent.model == "claude-opus-4-6"


def test_deidara():
    agent = deidara()
    assert agent.name == "Deidara"
    assert "root cause" in agent.instructions.lower()


def test_konan():
    agent = konan()
    assert agent.name == "Konan"
    assert "Documentation" in agent.instructions


def test_kakuzu():
    agent = kakuzu()
    assert agent.name == "Kakuzu"
    assert "CI/CD" in agent.instructions


# -- Customization --


def test_extra_instructions():
    agent = kisame(extra_instructions="Use Python 3.12 features.")
    assert "Python 3.12" in agent.instructions


def test_hidan_custom_model():
    agent = hidan(model="claude-sonnet-4-5-20250929")
    assert agent.model == "claude-sonnet-4-5-20250929"


# -- Teams --


def test_dev_team():
    team = dev_team()
    assert team.name == "Pain"
    assert len(team.handoffs) == 4
    member_names = {h.name for h in team.handoffs}
    assert member_names == {"Kisame", "Sasori", "Itachi", "Hidan"}


def test_full_team():
    team = full_team()
    assert team.name == "Pain"
    assert len(team.handoffs) == 8
    member_names = {h.name for h in team.handoffs}
    assert member_names == {
        "Kisame", "Tobi", "Sasori", "Itachi",
        "Hidan", "Deidara", "Konan", "Kakuzu",
    }


def test_dev_team_with_context():
    team = dev_team(extra_instructions="Stack: Next.js, Supabase, TypeScript")
    assert "Next.js" in team.instructions
