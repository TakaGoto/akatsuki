"""Pre-built agent presets you can use out of the box or customize."""

from __future__ import annotations

from typing import Any

from my_ai_team.agents.base import create_agent


def researcher(
    tools: list[Any] | None = None,
    extra_instructions: str = "",
) -> "Agent":
    """An agent specialized in research and information gathering."""
    return create_agent(
        name="Researcher",
        instructions=(
            "You are a thorough research agent. Gather information, verify facts, "
            "and provide well-sourced answers. Be concise but comprehensive.\n"
            + extra_instructions
        ),
        tools=tools,
    )


def coder(
    tools: list[Any] | None = None,
    extra_instructions: str = "",
) -> "Agent":
    """An agent specialized in writing and reviewing code."""
    return create_agent(
        name="Coder",
        instructions=(
            "You are an expert software engineer. Write clean, well-tested code. "
            "Follow best practices and keep solutions simple. Explain your approach briefly.\n"
            + extra_instructions
        ),
        tools=tools,
    )


def reviewer(
    tools: list[Any] | None = None,
    extra_instructions: str = "",
) -> "Agent":
    """An agent specialized in code review and quality assurance."""
    return create_agent(
        name="Reviewer",
        instructions=(
            "You are a senior code reviewer. Look for bugs, security issues, performance "
            "problems, and violations of best practices. Be specific and actionable.\n"
            + extra_instructions
        ),
        tools=tools,
    )


def writer(
    tools: list[Any] | None = None,
    extra_instructions: str = "",
) -> "Agent":
    """An agent specialized in writing documentation and content."""
    return create_agent(
        name="Writer",
        instructions=(
            "You are a technical writer. Write clear, concise documentation. "
            "Use simple language and provide practical examples.\n"
            + extra_instructions
        ),
        tools=tools,
    )
