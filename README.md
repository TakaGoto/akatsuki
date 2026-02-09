# My AI Team

Reusable AI agent patterns built on the [Anthropic Agent SDK](https://github.com/anthropics/agent-sdk). Drop these into any project to get a working team of AI agents.

## Install

```bash
pip install -e ".[dev]"
```

## Quick start

```python
import asyncio
from my_ai_team import create_agent
from my_ai_team.agents.base import run

agent = create_agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

asyncio.run(run(agent, "Hello!"))
```

## Create a team

```python
from my_ai_team import create_agent, create_team

researcher = create_agent(name="Researcher", instructions="You research topics.")
writer = create_agent(name="Writer", instructions="You write content.")

lead = create_team(
    name="Lead",
    instructions="Delegate research to Researcher, then writing to Writer.",
    members=[researcher, writer],
)
```

## Custom tools

```python
from my_ai_team import create_agent, tool

@tool
def search_web(query: str) -> str:
    """Search the web."""
    return do_search(query)

agent = create_agent(
    name="Researcher",
    instructions="Use your tools to find information.",
    tools=[search_web],
)
```

## Pre-built presets

```python
from my_ai_team.agents import researcher, coder, reviewer, writer

# Use as-is
my_reviewer = reviewer()

# Or customize
my_coder = coder(extra_instructions="Always use type hints.")
```

## Examples

See the [`examples/`](examples/) directory:

- `simple_agent.py` — single agent
- `team.py` — multi-agent team with handoffs
- `custom_tools.py` — agent with custom tools
- `presets.py` — using pre-built agent presets

## Setup

1. Copy `.env.example` to `.env` and add your Anthropic API key
2. `pip install -e ".[dev]"`
3. Run an example: `python examples/simple_agent.py`

## Tests

```bash
pytest
```

## License

MIT
