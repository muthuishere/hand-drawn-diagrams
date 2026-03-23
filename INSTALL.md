# Installation

**Jump to:** [npx skills add](#npx-skills-add) · [install.sh](#installsh) · [Manual](#manual) · [Uninstall](#uninstall)

## Prerequisites

- **Python 3.11+** — `python3 --version`
- **git** — `git --version`
- **uv** — `pip install uv` or `brew install uv`
- **Node.js + npm** (optional) — for fast PNG/video rendering via `chrome-devtools-mcp`

---

## npx skills add

The recommended way. Works for 40+ agents and handles project vs global scope.

```bash
# Project scope — committed with your repo, shared with team
npx skills add muthuishere/hand-drawn-diagrams

# Global scope — available in every project
npx skills add muthuishere/hand-drawn-diagrams -g

# Specific agents only
npx skills add muthuishere/hand-drawn-diagrams -a claude-code -a opencode
```

| Agent | Project path | Global path |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.codex/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |

Full agent list at [vercel-labs/skills](https://github.com/vercel-labs/skills).

---

## install.sh

For agents that follow the Claude / agent skills directory spec. Global scope only — installs based on which agent CLIs are detected on your `PATH`.

**macOS / Linux**

```bash
git clone https://github.com/muthuishere/hand-drawn-diagrams.git
cd hand-drawn-diagrams
bash install.sh
```

**Windows**

```cmd
git clone https://github.com/muthuishere/hand-drawn-diagrams.git
cd hand-drawn-diagrams
install.cmd
```

---

## Manual

For any agent not listed above, or if you prefer not to use npm. See [MANUAL-INSTALL.md](MANUAL-INSTALL.md) for per-agent copy commands and both project and global paths.

---

## Uninstall

**npx skills**

```bash
npx skills remove hand-drawn-diagrams      # project
npx skills remove hand-drawn-diagrams -g   # global
```

**install.sh** (macOS / Linux)

```bash
bash uninstall.sh
```

**install.sh** (Windows)

```cmd
uninstall.cmd
```

**Manual** — delete the directory you copied to, e.g.:

```bash
rm -rf ~/.claude/skills/hand-drawn-diagrams     # global
rm -rf .claude/skills/hand-drawn-diagrams       # project
```

---

## Optional: fast rendering

Install `chrome-devtools-mcp` for fast PNG and animated SVG export (real browser, no Playwright needed):

```bash
npm install -g chrome-devtools-mcp
```

For Claude Code, add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "chrome-devtools-mcp"
    }
  }
}
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uv: command not found` | `pip install uv` or `brew install uv` |
| `python: requires >=3.11` | Install Python 3.11+ and ensure it is first on `PATH` |
| Skill not found after install | Restart the agent / IDE session |
| Validation fails | Read the error from `validate_excalidraw.py` — usually a malformed JSON field |
| No hosted URL | Run `get_excalidraw_urls.py` only after validation exits 0 |
| Slow PNG render | Install `chrome-devtools-mcp` — Playwright fallback is much slower |
