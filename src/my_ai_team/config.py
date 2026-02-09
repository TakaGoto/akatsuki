"""Load project config from .akatsuki.yaml in the current directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG = {
    "team": "dev",
    "context": "",
    "agents": {},
}


def find_config(start: Path | None = None) -> Path | None:
    """Walk up from `start` (default: cwd) looking for .akatsuki.yaml."""
    current = start or Path.cwd()
    for directory in [current, *current.parents]:
        config_path = directory / ".akatsuki.yaml"
        if config_path.is_file():
            return config_path
    return None


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load and return the project config.

    If no path is given, searches upward from cwd. Returns defaults
    if no config file is found.
    """
    config_path = path or find_config()
    if config_path is None:
        return dict(DEFAULT_CONFIG)

    with open(config_path) as f:
        raw = yaml.safe_load(f) or {}

    return {
        "team": raw.get("team", DEFAULT_CONFIG["team"]),
        "context": raw.get("context", DEFAULT_CONFIG["context"]),
        "agents": raw.get("agents", DEFAULT_CONFIG["agents"]),
    }


def get_agent_overrides(config: dict[str, Any], agent_name: str) -> dict[str, str]:
    """Get per-agent overrides (extra instructions, model) from config.

    Returns a dict with optional keys: 'extra', 'model'.
    """
    agents = config.get("agents", {})
    return agents.get(agent_name, {})
