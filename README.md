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
# Install globally from GitHub
pip install git+https://github.com/TakaGoto/my-ai-team.git

# Or install locally for development (changes apply instantly)
pip install -e ~/my-ai-team
```

## CLI — use from any directory

```bash
# Default: uses the 4-agent dev team
myteam "add input validation to the signup form"

# Use a specific agent
myteam --agent feature-dev "refactor the auth module"
myteam --agent security-auditor "review this codebase"
myteam --agent bug-hunter "the login page crashes on empty email"

# Use the full 8-agent team
myteam --team full "add price alerts with tests and docs"

# Pass project context
myteam --context "Stack: Next.js, Supabase, TypeScript" "add a search endpoint"

# List all available agents and teams
myteam --list
```

## Python API

### Dev team

```python
import asyncio
from my_ai_team import dev_team
from my_ai_team.agents.base import run

# 4-agent team: Feature Dev -> Test Engineer -> Code Reviewer -> Security Auditor
team = dev_team(extra_instructions="Stack: Next.js, TypeScript, Supabase.")

asyncio.run(run(team, "Add input validation to the /api/users endpoint."))
```

### Full team

```python
from my_ai_team import full_team

team = full_team(extra_instructions="Monorepo with web and mobile apps.")
```

### Individual agents

```python
from my_ai_team.agents import feature_dev, code_reviewer, security_auditor

my_dev = feature_dev()
my_reviewer = code_reviewer(extra_instructions="Focus on React Server Components.")
my_security = security_auditor()  # uses Opus by default
my_security_lite = security_auditor(model="claude-sonnet-4-5-20250929")  # save costs
```

### Custom tools

```python
from my_ai_team import tool
from my_ai_team.agents import feature_dev

@tool
def run_typecheck() -> str:
    """Run TypeScript type checking."""
    return "0 errors"

agent = feature_dev(tools=[run_typecheck])
```

### Custom teams

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

- `dev_team.py` — standard 4-agent dev workflow
- `full_team.py` — all 8 agents
- `customize_agents.py` — project-specific tools and instructions
- `custom_tools.py` — agent with custom tools

## Setup

1. Copy `.env.example` to `.env` and add your Anthropic API key
2. `pip install -e ".[dev]"`
3. Run from terminal: `myteam "your task here"`

## Improving your agents

Edit the agents in `src/my_ai_team/agents/presets.py` to tweak prompts, change models, or add instructions. If you installed with `pip install -e`, changes apply immediately.

## Tests

```bash
pytest
```

## License

MIT
