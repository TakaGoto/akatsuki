"""CLI for running your AI agent team from any directory.

Usage:
    myteam "implement the signup form"
    myteam --agent feature-dev "add input validation"
    myteam --agent security-auditor "review this codebase"
    myteam --team dev "fix the login bug"
    myteam --team full "add price alerts with tests and docs"
    myteam --list
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from my_ai_team.agents.base import run
from my_ai_team.agents import presets
from my_ai_team.agents.teams import dev_team, full_team


AGENTS = {
    "tech-lead": presets.tech_lead,
    "feature-dev": presets.feature_dev,
    "mobile-dev": presets.mobile_dev,
    "test-engineer": presets.test_engineer,
    "code-reviewer": presets.code_reviewer,
    "security-auditor": presets.security_auditor,
    "bug-hunter": presets.bug_hunter,
    "docs-writer": presets.docs_writer,
    "devops": presets.devops,
}

TEAMS = {
    "dev": dev_team,
    "full": full_team,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="myteam",
        description="Run your AI agent team from the terminal.",
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
        "--team",
        choices=list(TEAMS.keys()),
        default="dev",
        help="Which team to use (default: dev).",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Extra project context to pass to the agent/team.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_agents",
        help="List all available agents and teams.",
    )
    return parser


def list_agents() -> None:
    print("Agents:")
    for name, factory in AGENTS.items():
        agent = factory()
        print(f"  {name:20s} {agent.name}")

    print("\nTeams:")
    for name, factory in TEAMS.items():
        team = factory()
        members = ", ".join(h.name for h in team.handoffs)
        print(f"  {name:20s} {team.name} -> [{members}]")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_agents:
        list_agents()
        return

    if not args.task:
        parser.print_help()
        sys.exit(1)

    if args.agent:
        factory = AGENTS[args.agent]
        agent = factory(extra_instructions=args.context)
    else:
        factory = TEAMS[args.team]
        agent = factory(extra_instructions=args.context)

    result = asyncio.run(run(agent, args.task))
    print(result)


if __name__ == "__main__":
    main()
