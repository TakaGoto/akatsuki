"""Core agent creation helpers."""

from __future__ import annotations

from typing import Any

from agents import Agent, Runner


def create_agent(
    name: str,
    instructions: str,
    tools: list[Any] | None = None,
    handoffs: list[Agent] | None = None,
    model: str = "claude-sonnet-4-5-20250929",
) -> Agent:
    """Create an agent with sensible defaults.

    Args:
        name: Display name for the agent.
        instructions: System prompt describing the agent's role.
        tools: List of tool functions decorated with @tool.
        handoffs: Other agents this agent can delegate to.
        model: Model ID to use. Defaults to Claude Sonnet 4.5.
    """
    return Agent(
        name=name,
        instructions=instructions,
        tools=tools or [],
        handoffs=handoffs or [],
        model=model,
    )


def create_team(
    name: str,
    instructions: str,
    members: list[Agent],
    model: str = "claude-sonnet-4-5-20250929",
) -> Agent:
    """Create a lead agent that orchestrates a team via handoffs.

    The lead agent can delegate work to any member agent. Members can
    hand back to the lead when their subtask is done.

    Args:
        name: Display name for the lead/orchestrator agent.
        instructions: System prompt for the lead agent.
        members: List of agents the lead can hand off to.
        model: Model ID for the lead agent.
    """
    return Agent(
        name=name,
        instructions=instructions,
        handoffs=members,
        model=model,
    )


async def run(agent: Agent, message: str) -> str:
    """Run an agent with a user message and return the final text output."""
    result = await Runner.run(agent, message)
    return result.final_output
