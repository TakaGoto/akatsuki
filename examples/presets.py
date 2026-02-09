"""Example: Use pre-built agent presets."""

import asyncio

from my_ai_team.agents import reviewer
from my_ai_team.agents.base import run


# Create a code reviewer with extra project-specific instructions
my_reviewer = reviewer(
    extra_instructions="Focus on Python best practices and type safety."
)


async def main():
    code = '''
def process(data):
    result = []
    for i in range(len(data)):
        if data[i] != None:
            result.append(data[i] * 2)
    return result
'''
    response = await run(my_reviewer, f"Review this code:\n```python{code}```")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
