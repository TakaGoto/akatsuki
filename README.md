# Akatsuki

Reusable AI agent team built on the [Anthropic Agent SDK](https://github.com/anthropics/agent-sdk). Each agent is named after an Akatsuki member whose abilities match their dev role.

## The Roster

| Member | Role | Ability | Access |
|--------|------|---------|--------|
| **Pain** | Tech Lead | Controls all paths — orchestrates the team | Full |
| **Kisame** | Feature Dev | Brute force — does the heavy implementation | Full |
| **Tobi** | Mobile Dev | Phases between dimensions — cross-platform | Full |
| **Sasori** | Test Engineer | Puppet master — controls test suites | Full |
| **Itachi** | Code Reviewer | Sharingan — sees every flaw | Read-only |
| **Hidan** | Security Auditor | Ritualist — methodical OWASP checklist | Read-only |
| **Deidara** | Bug Hunter | Art is an explosion — blows up bugs | Full |
| **Konan** | Docs Writer | Paper master — shapes documentation | Full |
| **Kakuzu** | DevOps | Five hearts — keeps multiple systems alive | Full |

## Install

```bash
pip install -e ~/my-ai-team
```

## CLI — use from any directory

```bash
# Default: Pain coordinates Kisame + Sasori + Itachi + Hidan
akatsuki "add input validation to the signup form"

# Send a specific agent
akatsuki --agent kisame "refactor the auth module"
akatsuki --agent hidan "review this codebase for vulnerabilities"
akatsuki --agent deidara "the login page crashes on empty email"
akatsuki --agent itachi "review the latest changes"

# Deploy the full squad
akatsuki --team full "add price alerts with tests and docs"

# Pass project context
akatsuki --context "Stack: Next.js, Supabase, TypeScript" "add a search endpoint"

# See the roster
akatsuki --list
```

## Python API

### Dev squad

```python
import asyncio
from my_ai_team import dev_team
from my_ai_team.agents.base import run

# Pain coordinates: Kisame -> Sasori -> Itachi -> Hidan
team = dev_team(extra_instructions="Stack: Next.js, TypeScript, Supabase.")

asyncio.run(run(team, "Add input validation to the /api/users endpoint."))
```

### Full Akatsuki

```python
from my_ai_team import full_team

team = full_team(extra_instructions="Monorepo with web and mobile apps.")
```

### Individual agents

```python
from my_ai_team.agents import kisame, itachi, hidan

my_dev = kisame()
my_reviewer = itachi(extra_instructions="Focus on React Server Components.")
my_security = hidan()  # uses Opus by default
my_security_lite = hidan(model="claude-sonnet-4-5-20250929")  # save costs
```

### Custom tools

```python
from my_ai_team import tool
from my_ai_team.agents import kisame

@tool
def run_typecheck() -> str:
    """Run TypeScript type checking."""
    return "0 errors"

agent = kisame(tools=[run_typecheck])
```

### Custom squad

```python
from my_ai_team import create_team
from my_ai_team.agents import kisame, sasori, hidan

team = create_team(
    name="Pain",
    instructions="1. Kisame implements\n2. Sasori tests\n3. Hidan reviews security",
    members=[kisame(), sasori(), hidan()],
)
```

## Examples

See [`examples/`](examples/):

- `dev_team.py` — core 4-agent squad
- `full_team.py` — all 8 agents under Pain
- `customize_agents.py` — project-specific tools and instructions
- `custom_tools.py` — agent with custom tools

## Setup

1. Copy `.env.example` to `.env` and add your Anthropic API key
2. `pip install -e ".[dev]"`
3. `akatsuki "your task here"`

## Improving your agents

Edit agents in `src/my_ai_team/agents/presets.py` — tweak prompts, swap models, add instructions. With `pip install -e`, changes apply instantly.

## Tests

```bash
pytest
```

## License

MIT
