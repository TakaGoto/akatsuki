"""CLI for running the Akatsuki agent team from any directory.

Usage:
    akatsuki "implement the signup form"
    akatsuki --agent kisame "add input validation"
    akatsuki --agents kisame,itachi,hidan "add auth with review"
    akatsuki --team full "add price alerts with tests and docs"
    akatsuki --list
    akatsuki --config
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from my_ai_team.agents.base import create_team, run
from my_ai_team.agents import presets
from my_ai_team.agents.teams import dev_team, full_team
from my_ai_team.config import load_config, get_agent_overrides


AGENTS = {
    "pain": presets.pain,
    "kisame": presets.kisame,
    "tobi": presets.tobi,
    "sasori": presets.sasori,
    "itachi": presets.itachi,
    "hidan": presets.hidan,
    "deidara": presets.deidara,
    "konan": presets.konan,
    "kakuzu": presets.kakuzu,
}

TEAMS = {
    "dev": dev_team,
    "full": full_team,
}

ROSTER = """
Akatsuki Dev Team
═══════════════════════════════════════
  Pain      Leader / Orchestrator
  Kisame    Feature Dev (implementation)
  Tobi      Mobile Dev (React Native)
  Sasori    Test Engineer (testing)
  Itachi    Code Reviewer (read-only)
  Hidan     Security Auditor (read-only)
  Deidara   Bug Hunter (debugging)
  Konan     Docs Writer (documentation)
  Kakuzu    DevOps (CI/CD, infra)

Teams
═══════════════════════════════════════
  dev       Kisame + Sasori + Itachi + Hidan
  full      All 8 agents under Pain
""".strip()


def build_agent_with_overrides(name: str, config: dict, cli_context: str = "") -> "Agent":
    """Build a single agent, applying .akatsuki.yaml overrides + CLI context."""
    factory = AGENTS[name]
    overrides = get_agent_overrides(config, name)

    extra = config.get("context", "")
    if overrides.get("extra"):
        extra += "\n" + overrides["extra"]
    if cli_context:
        extra += "\n" + cli_context

    kwargs = {"extra_instructions": extra}
    if overrides.get("model"):
        kwargs["model"] = overrides["model"]

    return factory(**kwargs)


def build_custom_squad(names: list[str], config: dict, cli_context: str = "") -> "Agent":
    """Build a Pain-led team from a list of agent names."""
    members = [build_agent_with_overrides(name, config, cli_context) for name in names]
    member_list = ", ".join(f"**{m.name}**" for m in members)

    context = config.get("context", "")
    if cli_context:
        context += "\n" + cli_context

    return create_team(
        name="Pain",
        instructions=(
            f"You are Pain, leader of a custom Akatsuki squad: {member_list}.\n\n"
            "Delegate tasks to the right specialist. "
            "Only mark complete when all agents have finished.\n\n"
            + context
        ),
        members=members,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="akatsuki",
        description="Run the Akatsuki AI agent team from the terminal.",
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="What you want the agent/team to do.",
    )
    parser.add_argument(
        "--agent",
        choices=list(AGENTS.keys()),
        help="Run a single agent.",
    )
    parser.add_argument(
        "--agents",
        help="Comma-separated list of agents for a custom squad (e.g. kisame,itachi,hidan).",
    )
    parser.add_argument(
        "--team",
        choices=list(TEAMS.keys()),
        help="Which pre-built team to use.",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Extra project context (added on top of .akatsuki.yaml context).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_agents",
        help="List all available agents and teams.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        dest="show_config",
        help="Show the loaded .akatsuki.yaml config for the current directory.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_agents:
        print(ROSTER)
        return

    config = load_config()

    if args.show_config:
        from my_ai_team.config import find_config
        config_path = find_config()
        if config_path:
            print(f"Config: {config_path}\n")
            print(f"Team:    {config['team']}")
            print(f"Context: {config['context'][:100]}{'...' if len(config['context']) > 100 else ''}")
            if config["agents"]:
                print("Agent overrides:")
                for name, overrides in config["agents"].items():
                    print(f"  {name}: {overrides}")
        else:
            print("No .akatsuki.yaml found in current directory or parents.")
        return

    if not args.task:
        parser.print_help()
        sys.exit(1)

    # Priority: --agent > --agents > --team > config team > default (dev)
    if args.agent:
        agent = build_agent_with_overrides(args.agent, config, args.context)
    elif args.agents:
        names = [n.strip() for n in args.agents.split(",")]
        invalid = [n for n in names if n not in AGENTS]
        if invalid:
            print(f"Unknown agents: {', '.join(invalid)}")
            print(f"Available: {', '.join(AGENTS.keys())}")
            sys.exit(1)
        agent = build_custom_squad(names, config, args.context)
    else:
        team_name = args.team or config.get("team", "dev")
        factory = TEAMS[team_name]
        context = config.get("context", "")
        if args.context:
            context += "\n" + args.context
        agent = factory(extra_instructions=context)

    result = asyncio.run(run(agent, args.task))
    print(result)


if __name__ == "__main__":
    main()
