"""Example: Use the full 8-agent team for complex tasks."""

import asyncio

from my_ai_team import full_team
from my_ai_team.agents.base import run


# The full team includes all specialists
team = full_team(
    extra_instructions=(
        "This is a monorepo with web apps (Next.js), mobile apps (React Native/Expo), "
        "and CLI tools (Node.js). All apps share a Supabase backend."
    )
)


async def main():
    response = await run(
        team,
        "Add a price alert feature that notifies users when a card hits their target price. "
        "This needs a database migration, API endpoint, UI component, tests, and docs.",
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
