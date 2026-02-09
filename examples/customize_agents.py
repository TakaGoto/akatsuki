"""Example: Customize individual Akatsuki agents for your project."""

import asyncio

from my_ai_team import create_team, tool
from my_ai_team.agents import kisame, sasori, hidan
from my_ai_team.agents.base import run


@tool
def run_typecheck() -> str:
    """Run TypeScript type checking."""
    return "Type check passed: 0 errors"


@tool
def run_tests() -> str:
    """Run the test suite."""
    return "42 tests passed, 0 failed"


# Customize agents for your specific project
my_kisame = kisame(
    tools=[run_typecheck],
    extra_instructions=(
        "Tech stack: Next.js 15, React 19, TypeScript 5, Supabase.\n"
        "Always run type checking after making changes.\n"
    ),
)

my_sasori = sasori(
    tools=[run_tests],
    extra_instructions=(
        "Use Vitest for all tests. Co-locate test files with source.\n"
        "Run tests after writing them to verify they pass.\n"
    ),
)

# Use sonnet instead of opus for Hidan to save costs
my_hidan = hidan(
    model="claude-sonnet-4-5-20250929",
    extra_instructions="Also check for Supabase RLS policy coverage.",
)

# Build a custom squad
team = create_team(
    name="Pain",
    instructions=(
        "Coordinate the squad:\n"
        "1. Kisame implements\n"
        "2. Sasori writes tests\n"
        "3. Hidan reviews security\n"
    ),
    members=[my_kisame, my_sasori, my_hidan],
)


async def main():
    response = await run(team, "Add rate limiting to the /api/search endpoint.")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
