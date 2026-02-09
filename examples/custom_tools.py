"""Example: Create an agent with custom tools."""

import asyncio

from my_ai_team import create_agent, tool
from my_ai_team.agents.base import run


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # Replace with a real API call
    return f"It's 72°F and sunny in {city}."


@tool
def get_time(timezone: str) -> str:
    """Get the current time in a timezone."""
    # Replace with a real implementation
    return f"The current time in {timezone} is 2:30 PM."


agent = create_agent(
    name="Travel Helper",
    instructions="You help people plan trips. Use your tools to provide real-time info.",
    tools=[get_weather, get_time],
)


async def main():
    response = await run(agent, "I'm heading to Tokyo tomorrow. What's the weather and time there?")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
