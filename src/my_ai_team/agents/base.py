"""Core agent creation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import sys

import litellm
from agents import Agent, Runner, RunConfig
from agents.extensions.models.litellm_provider import LitellmProvider
from agents.lifecycle import RunHooks
from agents.tracing import set_tracing_disabled

# Route all LLM calls through Anthropic via LiteLLM
litellm.modify_params = True
set_tracing_disabled(True)

ANTHROPIC_PROVIDER = RunConfig(model_provider=LitellmProvider())
MAX_TURNS = 50


class ProgressHooks(RunHooks):
    """Prints live progress to stderr so users see what agents are doing."""

    async def on_agent_start(self, context, agent):
        _log(f"[{agent.name}] starting...")

    async def on_tool_start(self, context, agent, tool):
        _log(f"  [{agent.name}] {tool.name}()")

    async def on_tool_end(self, context, agent, tool, result):
        preview = (result or "")[:80].replace("\n", " ").strip()
        if preview:
            _log(f"  [{agent.name}] {tool.name} -> {preview}")

    async def on_handoff(self, context, from_agent, to_agent):
        _log(f"[{from_agent.name}] -> [{to_agent.name}]")

    async def on_agent_end(self, context, agent, output):
        _log(f"[{agent.name}] done")


def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


HOOKS = ProgressHooks()


@dataclass
class TokenUsage:
    """Aggregated token usage across one or more agent runs."""
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0
    by_agent: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def add(self, agent_name: str, input_tokens: int, output_tokens: int, requests: int) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.requests += requests
        if agent_name in self.by_agent:
            self.by_agent[agent_name]["input_tokens"] += input_tokens
            self.by_agent[agent_name]["output_tokens"] += output_tokens
            self.by_agent[agent_name]["requests"] += requests
        else:
            self.by_agent[agent_name] = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "requests": requests,
            }

    def summary(self) -> str:
        lines = [
            "",
            "Token Usage",
            "═══════════════════════════════════════",
        ]
        for name, counts in self.by_agent.items():
            total = counts["input_tokens"] + counts["output_tokens"]
            lines.append(
                f"  {name:<16} {total:>8,} tokens "
                f"({counts['input_tokens']:,} in / {counts['output_tokens']:,} out) "
                f"[{counts['requests']} req]"
            )
        lines.append("───────────────────────────────────────")
        lines.append(
            f"  {'Total':<16} {self.total_tokens:>8,} tokens "
            f"({self.input_tokens:,} in / {self.output_tokens:,} out) "
            f"[{self.requests} req]"
        )
        return "\n".join(lines)


def create_agent(
    name: str,
    instructions: str,
    tools: list[Any] | None = None,
    handoffs: list[Agent] | None = None,
    model: str = "anthropic/claude-sonnet-4-5-20250929",
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
    model: str = "anthropic/claude-sonnet-4-5-20250929",
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


async def run(agent: Agent, message: str) -> tuple[str, TokenUsage]:
    """Run an agent with a user message and return (output, usage)."""
    result = await Runner.run(
        agent, message, run_config=ANTHROPIC_PROVIDER, max_turns=MAX_TURNS, hooks=HOOKS,
    )
    usage = TokenUsage()
    sdk_usage = result.context_wrapper.usage
    usage.add(
        agent_name=agent.name,
        input_tokens=sdk_usage.input_tokens,
        output_tokens=sdk_usage.output_tokens,
        requests=sdk_usage.requests,
    )
    return result.final_output, usage
