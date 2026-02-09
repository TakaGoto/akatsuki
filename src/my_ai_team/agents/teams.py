"""Pre-built Akatsuki team configurations for common workflows."""

from __future__ import annotations

from agents import Agent

from my_ai_team.agents.base import create_team
from my_ai_team.agents import presets


def dev_team(
    extra_instructions: str = "",
    kisame_tools: list | None = None,
    sasori_tools: list | None = None,
    itachi_tools: list | None = None,
    hidan_tools: list | None = None,
) -> Agent:
    """The core 4-agent Akatsuki squad: Kisame, Sasori, Itachi, Hidan
    — coordinated by Pain.

    Workflow:
    1. Kisame (Feature Dev) implements the changes
    2. Sasori (Test Engineer) writes tests
    3. Itachi (Code Reviewer) checks quality and patterns
    4. Hidan (Security Auditor) scans for vulnerabilities

    Args:
        extra_instructions: Additional context for Pain (e.g. your tech stack).
        kisame_tools: Tools for Kisame (Feature Dev).
        sasori_tools: Tools for Sasori (Test Engineer).
        itachi_tools: Tools for Itachi (Code Reviewer, should be read-only).
        hidan_tools: Tools for Hidan (Security Auditor, should be read-only).
    """
    return create_team(
        name="Pain",
        instructions=(
            "You are Pain, leader of the Akatsuki dev team. For every task:\n\n"
            "1. Hand off to **Kisame** to implement the changes\n"
            "2. Hand off to **Sasori** to write tests\n"
            "3. Hand off to **Itachi** to review quality\n"
            "4. Hand off to **Hidan** to check for vulnerabilities\n\n"
            "Only mark the task complete when ALL agents have finished and "
            "any issues they raised have been addressed.\n\n"
            + extra_instructions
        ),
        members=[
            presets.kisame(tools=kisame_tools),
            presets.sasori(tools=sasori_tools),
            presets.itachi(tools=itachi_tools),
            presets.hidan(tools=hidan_tools),
        ],
    )


def full_team(
    extra_instructions: str = "",
) -> Agent:
    """The full Akatsuki — all 8 specialists coordinated by Pain.

    Includes: Kisame (Feature Dev), Tobi (Mobile Dev), Sasori (Test),
    Itachi (Review), Hidan (Security), Deidara (Debug),
    Konan (Docs), Kakuzu (DevOps).
    """
    return create_team(
        name="Pain",
        instructions=(
            "You are Pain, leader of the full Akatsuki dev team. "
            "Assign tasks to the right specialist:\n\n"
            "- **Kisame** — implementation, bug fixes, refactoring\n"
            "- **Tobi** — mobile development (React Native / Expo)\n"
            "- **Sasori** — writing and fixing tests\n"
            "- **Itachi** — code review (read-only)\n"
            "- **Hidan** — security audit (read-only)\n"
            "- **Deidara** — debugging and root cause analysis\n"
            "- **Konan** — documentation\n"
            "- **Kakuzu** — CI/CD, deployment, infrastructure\n\n"
            "Delegate — don't do the work yourself. "
            "Run independent tasks in parallel when possible.\n\n"
            + extra_instructions
        ),
        members=[
            presets.kisame(),
            presets.tobi(),
            presets.sasori(),
            presets.itachi(),
            presets.hidan(),
            presets.deidara(),
            presets.konan(),
            presets.kakuzu(),
        ],
    )
