"""Pre-built team configurations for common workflows."""

from __future__ import annotations

from agents import Agent

from my_ai_team.agents.base import create_team
from my_ai_team.agents import presets


def dev_team(
    extra_instructions: str = "",
    feature_dev_tools: list | None = None,
    test_tools: list | None = None,
    review_tools: list | None = None,
    security_tools: list | None = None,
) -> Agent:
    """The standard 4-agent development team: Feature Dev, Test Engineer,
    Code Reviewer, and Security Auditor — coordinated by a Tech Lead.

    This is the core workflow used for implementing features and fixing bugs:
    1. Feature Dev implements the changes
    2. Test Engineer writes tests
    3. Code Reviewer checks quality and patterns
    4. Security Auditor scans for vulnerabilities

    Args:
        extra_instructions: Additional context for the Tech Lead (e.g. your tech stack).
        feature_dev_tools: Tools for the Feature Dev agent.
        test_tools: Tools for the Test Engineer agent.
        review_tools: Tools for the Code Reviewer (should be read-only).
        security_tools: Tools for the Security Auditor (should be read-only).
    """
    return create_team(
        name="Tech Lead",
        instructions=(
            "You coordinate a development team. For every task:\n\n"
            "1. Hand off to **Feature Dev** to implement the changes\n"
            "2. Hand off to **Test Engineer** to write tests\n"
            "3. Hand off to **Code Reviewer** to review quality\n"
            "4. Hand off to **Security Auditor** to check for vulnerabilities\n\n"
            "Only mark the task complete when ALL agents have finished and "
            "any issues they raised have been addressed.\n\n"
            + extra_instructions
        ),
        members=[
            presets.feature_dev(tools=feature_dev_tools),
            presets.test_engineer(tools=test_tools),
            presets.code_reviewer(tools=review_tools),
            presets.security_auditor(tools=security_tools),
        ],
    )


def full_team(
    extra_instructions: str = "",
) -> Agent:
    """The full 8-agent team with all specialists.

    Includes: Feature Dev, Mobile Dev, Test Engineer, Code Reviewer,
    Security Auditor, Bug Hunter, Docs Writer, and DevOps — all
    coordinated by a Tech Lead.
    """
    return create_team(
        name="Tech Lead",
        instructions=(
            "You coordinate a full development team. Assign tasks to the right specialist:\n\n"
            "- **Feature Dev**: Implementation, bug fixes, refactoring\n"
            "- **Mobile Dev**: React Native / mobile-specific work\n"
            "- **Test Engineer**: Writing and fixing tests\n"
            "- **Code Reviewer**: Quality review (read-only)\n"
            "- **Security Auditor**: Vulnerability scanning (read-only)\n"
            "- **Bug Hunter**: Debugging and root cause analysis\n"
            "- **Docs Writer**: Documentation\n"
            "- **DevOps**: CI/CD, deployment, infrastructure\n\n"
            "Delegate — don't do the work yourself. "
            "Run independent tasks in parallel when possible.\n\n"
            + extra_instructions
        ),
        members=[
            presets.feature_dev(),
            presets.mobile_dev(),
            presets.test_engineer(),
            presets.code_reviewer(),
            presets.security_auditor(),
            presets.bug_hunter(),
            presets.docs_writer(),
            presets.devops(),
        ],
    )
