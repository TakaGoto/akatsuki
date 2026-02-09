"""Tests for .akatsuki.yaml config loading."""

from pathlib import Path
from textwrap import dedent

from my_ai_team.config import load_config, find_config, get_agent_overrides


def test_load_config_defaults_when_no_file():
    config = load_config(path=Path("/nonexistent/.akatsuki.yaml"))
    # Falls back to defaults when file doesn't exist
    assert config["team"] == "dev"
    assert config["context"] == ""
    assert config["agents"] == {}


def test_load_config_from_yaml(tmp_path):
    yaml_file = tmp_path / ".akatsuki.yaml"
    yaml_file.write_text(dedent("""\
        team: full
        context: |
          Stack: Next.js, TypeScript, Supabase.
        agents:
          hidan:
            model: claude-sonnet-4-5-20250929
            extra: Check RLS policies.
          kisame:
            extra: Run pnpm check-types.
    """))

    config = load_config(path=yaml_file)
    assert config["team"] == "full"
    assert "Next.js" in config["context"]
    assert config["agents"]["hidan"]["model"] == "claude-sonnet-4-5-20250929"
    assert "RLS" in config["agents"]["hidan"]["extra"]
    assert "check-types" in config["agents"]["kisame"]["extra"]


def test_find_config_walks_up(tmp_path):
    # Create config in parent
    yaml_file = tmp_path / ".akatsuki.yaml"
    yaml_file.write_text("team: dev\n")

    # Search from a subdirectory
    sub = tmp_path / "src" / "app"
    sub.mkdir(parents=True)

    found = find_config(start=sub)
    assert found == yaml_file


def test_find_config_returns_none_when_missing(tmp_path):
    found = find_config(start=tmp_path)
    assert found is None


def test_get_agent_overrides():
    config = {
        "agents": {
            "hidan": {"model": "claude-sonnet-4-5-20250929", "extra": "Check RLS."},
        }
    }
    assert get_agent_overrides(config, "hidan") == {
        "model": "claude-sonnet-4-5-20250929",
        "extra": "Check RLS.",
    }
    assert get_agent_overrides(config, "kisame") == {}


def test_load_config_handles_empty_yaml(tmp_path):
    yaml_file = tmp_path / ".akatsuki.yaml"
    yaml_file.write_text("")

    config = load_config(path=yaml_file)
    assert config["team"] == "dev"
    assert config["context"] == ""
