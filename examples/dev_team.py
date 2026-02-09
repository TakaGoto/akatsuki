"""Example: Use the standard 4-agent dev team workflow.

This is the core workflow from punk_records:
  Feature Dev → Test Engineer → Code Reviewer → Security Auditor
"""

import asyncio

from my_ai_team import dev_team
from my_ai_team.agents.base import run


# Create a dev team customized for your project
team = dev_team(
    extra_instructions=(
        "Tech stack: Next.js 15, React 19, TypeScript, Supabase.\n"
        "Monorepo with pnpm workspaces and Turborepo.\n"
    )
)


async def main():
    response = await run(
        team,
        "Add input validation to the /api/users POST endpoint. "
        "It should validate email format and require a name field.",
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
