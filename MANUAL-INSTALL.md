# Manual Installation

For agents not supported by `install.sh` or `npx skills add`, copy the skill files directly into the agent's skills directory.

## Step 1 — Clone

```bash
git clone https://github.com/muthuishere/hand-drawn-diagrams.git ~/.hand-drawn-diagrams
```

## Step 2 — Copy to the agent's skills directory

### Global (available in every project)

| Agent | Path |
|---|---|
| Claude Code | `~/.claude/skills/hand-drawn-diagrams/` |
| Codex | `~/.codex/skills/hand-drawn-diagrams/` |
| OpenCode | `~/.config/opencode/skills/hand-drawn-diagrams/` |
| Windsurf | `~/.codeium/windsurf/skills/hand-drawn-diagrams/` |
| GitHub Copilot | `~/.copilot/skills/hand-drawn-diagrams/` |
| Cursor | `~/.cursor/skills/hand-drawn-diagrams/` |
| Gemini CLI | `~/.gemini/skills/hand-drawn-diagrams/` |

```bash
# Example: Claude Code global
mkdir -p ~/.claude/skills
cp -r ~/.hand-drawn-diagrams ~/.claude/skills/hand-drawn-diagrams
```

### Project (committed with your repo, shared with team)

| Agent | Path |
|---|---|
| Claude Code | `.claude/skills/hand-drawn-diagrams/` |
| Codex | `.agents/skills/hand-drawn-diagrams/` |
| OpenCode | `.agents/skills/hand-drawn-diagrams/` |
| Windsurf | `.windsurf/skills/hand-drawn-diagrams/` |
| GitHub Copilot | `.agents/skills/hand-drawn-diagrams/` |
| Cursor | `.agents/skills/hand-drawn-diagrams/` |

```bash
# Example: Claude Code project
mkdir -p .claude/skills
cp -r ~/.hand-drawn-diagrams .claude/skills/hand-drawn-diagrams
```

Commit the directory to share the skill with your team.

## Uninstall

Delete the directory you copied to:

```bash
# Claude Code global
rm -rf ~/.claude/skills/hand-drawn-diagrams

# Claude Code project
rm -rf .claude/skills/hand-drawn-diagrams
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uv: command not found` | `pip install uv` or `brew install uv` |
| `python: requires >=3.11` | Install Python 3.11+ and ensure it is first on `PATH` |
| Skill not found after install | Restart the agent / IDE session |
| Validation fails | Read the error from `validate_excalidraw.py` — usually a malformed JSON field |
| No hosted URL | Run `get_excalidraw_urls.py` only after validation exits 0 |
| Slow PNG render | Install `chrome-devtools-mcp` — Playwright fallback is much slower |
