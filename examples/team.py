"""Example: Create a team of agents that collaborate via handoffs."""

import asyncio

from my_ai_team import create_agent, create_team
from my_ai_team.agents.base import run


# Define specialized agents
researcher = create_agent(
    name="Researcher",
    instructions=(
        "You research topics thoroughly and provide factual summaries. "
        "When you're done researching, hand off to the Writer to draft the final output."
    ),
)

writer = create_agent(
    name="Writer",
    instructions=(
        "You take research notes and turn them into polished, readable content. "
        "Keep it concise and engaging."
    ),
)

# Create a lead agent that can delegate to the team
lead = create_team(
    name="Team Lead",
    instructions=(
        "You coordinate a small team. For any question:\n"
        "1. Hand off to Researcher to gather information\n"
        "2. Hand off to Writer to produce the final answer\n"
        "Delegate — don't do the work yourself."
    ),
    members=[researcher, writer],
)


async def main():
    response = await run(lead, "Write a brief explainer on how AI agents work.")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
