"""Example: Create and run a single agent."""

import asyncio

from my_ai_team import create_agent
from my_ai_team.agents.base import run


agent = create_agent(
    name="Assistant",
    instructions="You are a helpful assistant. Keep answers short and practical.",
)


async def main():
    response = await run(agent, "What are 3 tips for writing clean Python code?")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
