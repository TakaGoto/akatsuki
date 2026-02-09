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
pip install -e ~/akatsuki
```

## CLI — use from any directory

```bash
# Default: Pain coordinates Kisame + Sasori + Itachi + Hidan
akatsuki "add input validation to the signup form"

# Send a specific agent
akatsuki --agent kisame "refactor the auth module"
akatsuki --agent hidan "review this codebase for vulnerabilities"
akatsuki --agent deidara "the login page crashes on empty email"

# Mix and match a custom squad
akatsuki --agents kisame,itachi "quick implementation with review"
akatsuki --agents kisame,sasori,hidan "build with tests and security"
akatsuki --agents tobi,sasori,itachi "mobile feature with tests and review"

# Deploy the full squad
akatsuki --team full "add price alerts with tests and docs"

# Pass extra context
akatsuki --context "Use Zod for validation" "add input validation"

# See the roster
akatsuki --list

# Check loaded project config
akatsuki --config
```

## Project config — `.akatsuki.yaml`

Drop an `.akatsuki.yaml` in any project root. The CLI auto-detects it (walks up from cwd) and applies it to every command — no flags needed.

```yaml
# .akatsuki.yaml
team: dev
context: |
  Monorepo with pnpm workspaces and Turborepo.
  Stack: Next.js 15, React 19, TypeScript 5, Supabase.
  Mobile apps use React Native / Expo SDK 54.

agents:
  hidan:
    model: claude-sonnet-4-5-20250929   # save costs
    extra: "Check Supabase RLS policies."
  kisame:
    extra: "Run pnpm check-types after changes."
  tobi:
    extra: "Apps: loki, ace. Use Zustand + AsyncStorage."
```

Then just:
```bash
cd ~/my-project
akatsuki "add user authentication"
# Picks up team, context, and agent overrides automatically
```

### Config fields

| Field | Type | Description |
|-------|------|-------------|
| `team` | `dev` or `full` | Default team when no `--team`/`--agent`/`--agents` flag is used |
| `context` | string | Project context injected into every agent's instructions |
| `agents` | map | Per-agent overrides |
| `agents.<name>.extra` | string | Additional instructions for that agent |
| `agents.<name>.model` | string | Override the model for that agent |

### Config priority

CLI flags always win over `.akatsuki.yaml`:
```
--agent/--agents/--team  >  .akatsuki.yaml team  >  default (dev)
--context                +  .akatsuki.yaml context  (combined, not replaced)
```

## Python API

### Dev squad

```python
import asyncio
from my_ai_team import dev_team
from my_ai_team.agents.base import run

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
