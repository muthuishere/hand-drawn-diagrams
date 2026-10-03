# CLAUDE.md

## Project Overview

**hand-drawn-diagrams** is an AI skill that converts natural language prompts into hand-drawn Excalidraw diagrams. It produces a hosted edit URL, animated SVG, and PNG — from a single prompt, no app required.

This repository contains the skill definition, rendering scripts, and installer for Claude Code and compatible agents.

## Repository Structure

```
hand-drawn-diagrams/
├── SKILL.md                    # Skill entry point (name + description)
├── workflow.md                 # Master workflow — read this first
├── steps/
│   ├── step-01-route.md        # Pick diagram type from routing table
│   ├── step-02-draw.md         # Generate .excalidraw + .animationinfo.json
│   └── step-03-validate.md     # Validate, get hosted URL, offer animation
├── references/
│   ├── activation-routing.xml  # Route selection rules
│   ├── fundamental-shapes.md   # Core shape language
│   ├── json-schema.md          # .excalidraw JSON schema
│   ├── element-templates.md    # Grid layout + element templates
│   ├── animation-spec.md       # Animation story patterns
│   ├── quality-checklist.md    # Diagram quality rules
│   ├── patterns.md             # Reusable layout patterns
│   └── *-diagrams.md           # Per-route guides (teachers, ux, funnel…)
├── scripts/                    # Python rendering tools (managed with uv)
│   ├── validate_excalidraw.py  # Pre-flight validation — run before URL gen
│   ├── get_excalidraw_urls.py  # Generates hosted Edit + Animate URLs
│   ├── edit_excalidraw.py      # Opens diagram in hosted editor
│   ├── render_excalidraw.py    # PNG export (Playwright fallback)
│   ├── render_animated_svg.py  # Animated SVG export (Playwright fallback)
│   ├── animate_excalidraw.py   # Animation helper
│   ├── hosted_scene_urls.py    # URL encoding utilities
│   ├── local_excalidraw_server.py
│   ├── pyproject.toml          # Python deps: playwright>=1.40, pytest
│   └── tests/                  # pytest test suite
├── installscripts/
│   ├── install.py              # Detects Claude Code / Agent CLI, installs skill
│   └── uninstall.py
├── install.sh / install.cmd    # Shell wrappers → installscripts/install.py
├── uninstall.sh / uninstall.cmd
└── docs/                       # Additional documentation
```

## Tech Stack

- **Language**: Python 3.11+
- **Package manager**: `uv` (always use `uv run python ...` for scripts)
- **Rendering**: Chrome DevTools MCP (preferred) or Playwright (fallback)
- **Output format**: `.excalidraw` JSON, `.animationinfo.json`, `.animated.svg`, `.png`
- **Diagram host**: Excalidraw hosted editor (gzip/base64 scene in URL hash)

## Skill Activation

The skill is activated via `SKILL.md`. When activated, it follows `workflow.md`:

1. **Route** (`step-01-route.md`) — pick one diagram type
2. **Draw** (`step-02-draw.md`) — write `.excalidraw` + `.animationinfo.json`
3. **Validate** (`step-03-validate.md`) — validate, generate hosted URL, deliver

## Key Conventions

### File locations
- `.excalidraw` + `.animationinfo.json` → `/tmp/hand-drawn-diagrams/<slug>/` (never litter workspace)
- `.animated.svg` → **always** the user's project/workspace directory
- Write to workspace only if user specifies a path

### Rendering commands (always run from `scripts/`)
```bash
cd scripts
uv run python validate_excalidraw.py "/absolute/path/to/file.excalidraw"
uv run python open_diagram.py "/absolute/path/to/file.excalidraw"   # preferred: writes open.html + opens browser
uv run python get_excalidraw_urls.py "/absolute/path/to/file.excalidraw"  # fallback: prints raw URLs
uv run python render_excalidraw.py "/absolute/path/to/file.excalidraw"
uv run python render_animated_svg.py "/tmp/.../diagram.excalidraw" --output "/project/name.animated.svg"
```

### Rendering priority
1. Chrome DevTools MCP — fast, uses real browser, no install required
2. Playwright scripts — fallback only

### Output delivery order
1. Hosted edit URL (always first, after validation passes)
2. Offer animation ("Want a video version?")
3. PNG only if explicitly requested

### Diagram style defaults
- Hand-drawn / sketch font
- Monochrome (no fills unless essential)
- Files go to `/tmp/` — workspace stays clean

## Running Tests

```bash
cd scripts
uv run pytest                          # all tests
uv run pytest -m "not slow"            # skip Playwright/Chromium tests
uv run pytest tests/test_validate_excalidraw.py
```

## Installation / Uninstall

```bash
bash install.sh      # macOS/Linux — detects Claude Code and Agent CLI
install.cmd          # Windows
bash uninstall.sh    # macOS/Linux
uninstall.cmd        # Windows
```

## What NOT to do

- Do not write `.excalidraw` files to the user's workspace without being asked
- Do not run `get_excalidraw_urls.py` before `validate_excalidraw.py` exits 0
- Do not render before the `.excalidraw` file is written and validated
- Do not use `excalidraw.com` directly — use `edit_excalidraw.py` to get hosted URLs
- Do not add multiple colors/fills for decoration — keep diagrams monochrome by default
- Do not write paragraphs inside shapes — diagrams use 1–5 word labels only

<!-- ctx-optimize:begin -->
<ctx-optimize>
  <precondition>Run `command -v ctx-optimize` first. If it is NOT installed, IGNORE this entire
  block and answer by reading the code normally — the store is an optimization, not a requirement
  (install later with `npm install -g @muthuishere/ctx-optimize`, or download the binary). Everything
  below applies ONLY when the command exists.</precondition>
  <store>MULTI-MODULE repo, pre-built knowledge store at `~/ctxoptimize/hand-drawn-diagrams/` — one graph per module + a navigator, 1 modules declared in `.ctxoptimize/config.json`.</store>
  <use>Use it INSTEAD of grep-and-read chains — PICK BY INTENT: find → `ctx-optimize query "<terms>"` ·
  inspect a symbol → `card <symbol>` · about to EDIT → `change-plan <symbol>` (callers+impact+tests, one
  call) · blast radius → `affected <symbol>` · connection → `path <a> <b>` ·
  list/filter (no jq): `nodes --kind K` / `edges --relation R` / `deps --scope dev`.
  Scope follows your cwd: a module dir answers from that module (zero hits escalate repo-wide); the root
  federates via the navigator (`~/ctxoptimize/hand-drawn-diagrams/navigator.md`; `--modules all|a,b` widens).
  Output is parsed fact with exact file:line — cite it directly, do NOT re-verify in source.
  Exhaustive literal-string sweeps stay grep's job.</use>
  <deep-doc>The FULL usage card — verify discipline, store-vs-grep ladder, sources (databases/
  buckets/queues/APIs by env-var name), remote push/pull, `up` — is committed at
  `.ctxoptimize/instructions.md`. Read it before deeper store work.</deep-doc>
  <no-local-store>Fresh clone with nothing at `~/ctxoptimize/hand-drawn-diagrams/`? Run `ctx-optimize up` —
  it pulls the team's prebuilt store when the config declares one, otherwise rebuilds every module store in seconds.</no-local-store>
</ctx-optimize>
<!-- ctx-optimize:end -->
