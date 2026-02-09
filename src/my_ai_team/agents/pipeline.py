"""Pipeline execution — run agents in stages with parallel support.

A pipeline is a sequence of stages. Each stage runs one or more agents.
When a stage has multiple agents, they run in parallel via asyncio.gather.
Output from each stage is passed as context to the next.

Fix stages receive review findings and are instructed to address them.

Example:
    Kisame (implement) → [Sasori, Itachi, Hidan] (parallel review) → Kisame (fix)
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from agents import Agent, Runner


@dataclass
class Stage:
    """A pipeline stage with one or more agents that run in parallel."""
    agents: list[Agent]
    label: str = ""
    fix: bool = False


@dataclass
class Pipeline:
    """A sequence of stages executed in order.

    Within each stage, agents run in parallel. Output from one stage
    becomes context for the next. Stages marked with fix=True get
    a modified prompt asking the agent to address findings.
    """
    stages: list[Stage]
    context: str = ""


async def _run_agent(agent: Agent, message: str) -> tuple[str, str]:
    """Run a single agent and return (agent_name, output)."""
    result = await Runner.run(agent, message)
    return agent.name, result.final_output


def _build_message(
    context: str,
    task: str,
    previous_outputs: list[tuple[str, str]],
    is_fix: bool = False,
) -> str:
    """Build the prompt message for a stage."""
    parts = []
    if context:
        parts.append(f"Project context:\n{context}")

    parts.append(f"Task: {task}")

    if previous_outputs:
        prev = "\n\n".join(
            f"### {name}\n{output}" for name, output in previous_outputs
        )
        parts.append(f"## Previous stage output\n{prev}")

    if is_fix:
        parts.append(
            "## Your mission\n"
            "The review stage above found issues in the implementation. "
            "Go through EVERY issue raised by the reviewers and fix them. "
            "For each issue:\n"
            "1. Identify the file and problem\n"
            "2. Apply the fix\n"
            "3. Confirm it's resolved\n\n"
            "If a reviewer approved with no issues, skip their section. "
            "Only address actual problems that need code changes."
        )

    return "\n\n".join(parts)


async def run_pipeline(pipeline: Pipeline, task: str) -> str:
    """Execute a pipeline: stages run sequentially, agents within a stage run in parallel.

    Returns a combined summary of all agent outputs.
    """
    all_outputs: list[tuple[str, str]] = []

    for stage in pipeline.stages:
        message = _build_message(
            context=pipeline.context,
            task=task,
            previous_outputs=all_outputs,
            is_fix=stage.fix,
        )

        if len(stage.agents) == 1:
            name, output = await _run_agent(stage.agents[0], message)
            all_outputs.append((name, output))
            label = stage.label or name
            if stage.fix:
                print(f"[{label}] fixing issues...")
            print(f"[{label}] done")
        else:
            label = stage.label or ", ".join(a.name for a in stage.agents)
            print(f"[{label}] running {len(stage.agents)} agents in parallel...")
            results = await asyncio.gather(
                *[_run_agent(agent, message) for agent in stage.agents]
            )
            for name, output in results:
                all_outputs.append((name, output))
                print(f"  [{name}] done")

    # Combine all outputs into a final summary
    sections = []
    for name, output in all_outputs:
        sections.append(f"## {name}\n\n{output}")

    return "\n\n---\n\n".join(sections)
