"""Example: Customize individual agents for your project.

Shows how to tailor agents with project-specific instructions,
custom tools, and different model choices.
"""

import asyncio

from my_ai_team import create_team, tool
from my_ai_team.agents import feature_dev, test_engineer, security_auditor
from my_ai_team.agents.base import run


# Add project-specific tools
@tool
def run_typecheck() -> str:
    """Run TypeScript type checking."""
    # Replace with actual command execution
    return "Type check passed: 0 errors"


@tool
def run_tests() -> str:
    """Run the test suite."""
    # Replace with actual command execution
    return "42 tests passed, 0 failed"


# Customize agents for your specific project
my_feature_dev = feature_dev(
    tools=[run_typecheck],
    extra_instructions=(
        "Tech stack: Next.js 15, React 19, TypeScript 5, Supabase.\n"
        "Always run type checking after making changes.\n"
    ),
)

my_test_engineer = test_engineer(
    tools=[run_tests],
    extra_instructions=(
        "Use Vitest for all tests. Co-locate test files with source.\n"
        "Run tests after writing them to verify they pass.\n"
    ),
)

# Use sonnet instead of opus for security to save costs
my_security = security_auditor(
    model="claude-sonnet-4-5-20250929",
    extra_instructions="Also check for Supabase RLS policy coverage.",
)

# Build a custom team with your configured agents
team = create_team(
    name="My Tech Lead",
    instructions=(
        "Coordinate the team:\n"
        "1. Feature Dev implements\n"
        "2. Test Engineer writes tests\n"
        "3. Security Auditor reviews\n"
    ),
    members=[my_feature_dev, my_test_engineer, my_security],
)


async def main():
    response = await run(team, "Add rate limiting to the /api/search endpoint.")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
