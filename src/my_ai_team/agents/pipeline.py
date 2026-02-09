"""Pipeline execution — run agents in stages with parallel support.

A pipeline is a sequence of stages. Each stage runs one or more agents.
When a stage has multiple agents, they run in parallel via asyncio.gather.
Output from each stage is passed as context to the next.

Example:
    Kisame (implement) → [Sasori, Itachi, Hidan] (parallel review)
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


@dataclass
class Pipeline:
    """A sequence of stages executed in order.

    Within each stage, agents run in parallel. Output from one stage
    becomes context for the next.
    """
    stages: list[Stage]
    context: str = ""


async def _run_agent(agent: Agent, message: str) -> tuple[str, str]:
    """Run a single agent and return (agent_name, output)."""
    result = await Runner.run(agent, message)
    return agent.name, result.final_output


async def run_pipeline(pipeline: Pipeline, task: str) -> str:
    """Execute a pipeline: stages run sequentially, agents within a stage run in parallel.

    Returns a combined summary of all agent outputs.
    """
    all_outputs: list[tuple[str, str]] = []
    current_context = ""

    if pipeline.context:
        current_context = f"Project context:\n{pipeline.context}\n\n"

    for i, stage in enumerate(pipeline.stages):
        # Build the message for this stage
        message = f"{current_context}Task: {task}"
        if all_outputs:
            prev = "\n\n".join(
                f"### {name}\n{output}" for name, output in all_outputs
            )
            message = (
                f"{current_context}"
                f"Task: {task}\n\n"
                f"## Previous stage output\n{prev}"
            )

        if len(stage.agents) == 1:
            # Single agent — run directly
            name, output = await _run_agent(stage.agents[0], message)
            all_outputs.append((name, output))
            label = stage.label or name
            print(f"[{label}] done")
        else:
            # Multiple agents — run in parallel
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
