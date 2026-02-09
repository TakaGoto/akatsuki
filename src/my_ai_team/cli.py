"""CLI for running the Akatsuki agent team from any directory.

Usage:
    akatsuki "implement the signup form"
    akatsuki --agent kisame "add input validation"
    akatsuki --agent hidan "review this codebase for vulnerabilities"
    akatsuki --team dev "fix the login bug"
    akatsuki --team full "add price alerts with tests and docs"
    akatsuki --list
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from my_ai_team.agents.base import run
from my_ai_team.agents import presets
from my_ai_team.agents.teams import dev_team, full_team


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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_agents:
        print(ROSTER)
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
