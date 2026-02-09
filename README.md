# My AI Team

Reusable AI agent patterns built on the [Anthropic Agent SDK](https://github.com/anthropics/agent-sdk). Drop these into any project to get a working team of AI agents.

## Agents

| Agent | Role | Access |
|-------|------|--------|
| **Tech Lead** | Orchestrator — decomposes tasks and assigns to specialists | Full |
| **Feature Dev** | Implements features, bug fixes, refactoring | Full |
| **Mobile Dev** | React Native / Expo mobile development | Full |
| **Test Engineer** | Unit, integration, and E2E tests | Full |
| **Code Reviewer** | Quality, patterns, performance review | Read-only |
| **Security Auditor** | OWASP Top 10 vulnerability scanning | Read-only |
| **Bug Hunter** | Debugging and root cause analysis | Full |
| **Docs Writer** | Documentation and technical writing | Full |
| **DevOps** | CI/CD, deployment, infrastructure | Full |

## Install

```bash
pip install -e ".[dev]"
```

## Quick start — dev team

The fastest way to get a working agent team:

```python
import asyncio
from my_ai_team import dev_team
from my_ai_team.agents.base import run

# 4-agent team: Feature Dev → Test Engineer → Code Reviewer → Security Auditor
team = dev_team(extra_instructions="Stack: Next.js, TypeScript, Supabase.")

asyncio.run(run(team, "Add input validation to the /api/users endpoint."))
```

## Full team

All 8 specialist agents coordinated by a Tech Lead:

```python
from my_ai_team import full_team

team = full_team(extra_instructions="Monorepo with web and mobile apps.")
```

## Use agents individually

```python
from my_ai_team.agents import feature_dev, code_reviewer, security_auditor

# Use as-is
my_dev = feature_dev()

# Or customize for your project
my_reviewer = code_reviewer(extra_instructions="Focus on React Server Components.")

# Security auditor uses Opus by default for deeper analysis
my_security = security_auditor()

# Override model to save costs
my_security_lite = security_auditor(model="claude-sonnet-4-5-20250929")
```

## Custom tools

```python
from my_ai_team import tool
from my_ai_team.agents import feature_dev

@tool
def run_typecheck() -> str:
    """Run TypeScript type checking."""
    return "0 errors"

agent = feature_dev(tools=[run_typecheck])
```

## Build custom teams

```python
from my_ai_team import create_team
from my_ai_team.agents import feature_dev, test_engineer, security_auditor

team = create_team(
    name="My Lead",
    instructions="1. Feature Dev implements\n2. Tests\n3. Security review",
    members=[feature_dev(), test_engineer(), security_auditor()],
)
```

## Examples

See [`examples/`](examples/):

- `simple_agent.py` — single agent
- `dev_team.py` — standard 4-agent dev workflow
- `full_team.py` — all 8 agents
- `customize_agents.py` — project-specific tools and instructions
- `custom_tools.py` — agent with custom tools

## Setup

1. Copy `.env.example` to `.env` and add your Anthropic API key
2. `pip install -e ".[dev]"`
3. Run an example: `python examples/dev_team.py`

## Tests

```bash
pytest
```

## License

MIT
