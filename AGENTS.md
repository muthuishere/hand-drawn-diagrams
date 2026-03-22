# AGENTS.md

## Project: hand-drawn-diagrams

AI skill that converts natural language prompts into hand-drawn Excalidraw diagrams with hosted edit URLs, animated SVGs, and PNGs.

## Agent Workflow

This skill follows a strict 3-step process. **Never skip steps or reorder them.**

### Step 1 — Route (`steps/step-01-route.md`)
Pick one diagram type from the routing table:

| Route | Keywords |
|---|---|
| `teachers` | teach, explain simply, lesson, compare, ELI5 |
| `ideation` | brainstorm, cluster notes, opportunity map |
| `ux` | journey, wireflow, sitemap, screen flow |
| `sales-funnel` | funnel, drop-off, conversion, leads |
| `technical-explainer` | architecture, API, protocol, event flow |
| `medical` | condition, diagnosis, treatment, patient |
| `creative-raw` | open/explicit creative mode |
| `page-mockup` | webpage, dashboard, landing page, UI |

Load `references/activation-routing.xml` and `references/fundamental-shapes.md` first, then one route guide from `references/`.

### Step 2 — Draw (`steps/step-02-draw.md`)
Write two files (in `/tmp/hand-drawn-diagrams/<slug>/` by default):
1. `diagram.excalidraw` — complete `.excalidraw` JSON with non-empty `elements` array
2. `diagram.animationinfo.json` — animation spec with story pattern and element order

Both files must exist before Step 3 begins.

### Step 3 — Validate & Deliver (`steps/step-03-validate.md`)

```bash
# 1. Validate first — fix all errors before proceeding
cd scripts && uv run python validate_excalidraw.py "/tmp/hand-drawn-diagrams/<slug>/diagram.excalidraw"

# 2. Generate hosted URLs only after validation passes
cd scripts && uv run python get_excalidraw_urls.py "/tmp/hand-drawn-diagrams/<slug>/diagram.excalidraw"
```

Deliver the full Edit URL as a clickable link. Offer animation at the end.

## Tool Usage

### Rendering tools (always `cd scripts` first, use `uv run`)

| Tool | When to use |
|---|---|
| `validate_excalidraw.py` | Always — before URL generation |
| `open_diagram.py` | After validation — writes `open.html`, opens browser, prints short local path |
| `get_excalidraw_urls.py` | Fallback only — prints raw hosted URLs when `open_diagram.py` unavailable |
| `edit_excalidraw.py` | Open diagram directly in hosted editor (legacy) |
| `render_excalidraw.py` | PNG export (Playwright fallback) |
| `render_animated_svg.py` | Animated SVG (Playwright fallback) |

### Chrome DevTools MCP (preferred over Playwright)
Use when available for PNG and animated SVG rendering:
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__new_page`
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__navigate_page`
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__wait_for`
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__evaluate_script` (extract SVG)
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__take_screenshot` (PNG)
- `mcp__plugin_chrome-devtools-mcp_chrome-devtools__close_page`

### Excalidraw MCP (for checkpointing)
- `mcp__claude_ai_excalidraw__export_to_excalidraw`
- `mcp__claude_ai_excalidraw__create_view`
- `mcp__claude_ai_excalidraw__save_checkpoint` / `read_checkpoint`

## File Location Rules

| Artifact | Default location |
|---|---|
| `.excalidraw` | `/tmp/hand-drawn-diagrams/<slug>/diagram.excalidraw` |
| `.animationinfo.json` | `/tmp/hand-drawn-diagrams/<slug>/diagram.animationinfo.json` |
| `.animated.svg` | User's current project/workspace directory |
| `.png` | User's current project/workspace directory |

Write to workspace only if the user specifies a path or explicitly asks.

## Diagram Rules

- **Monochrome by default** — no fills unless essential for clarity
- **Sketch font** — same font across all elements
- **1–5 word labels** — never write sentences or paragraphs inside shapes
- **No floating arrows** — bind with `startBinding`/`endBinding`
- **Bind text to containers** — use `containerId` + `boundElements`
- **One concept per box** — split instead of cramming
- **Non-overlapping layout** — use grid from `references/element-templates.md`

## Delivery Pattern

1. Run `open_diagram.py` — opens browser with `open.html` launcher. Deliver the printed local path as `[Open diagram](file:///tmp/.../open.html)`. **Never paste the raw hosted URL** — it is too long to be usable.
2. Offer: "Want a video version? I can render it as an animated diagram (~10s)"
3. If in `/tmp`, offer: "Want me to save the source file to your project?"
4. PNG only if user explicitly asked for an image

## Critical Rules

1. **Never render before the `.excalidraw` file exists and validates clean**
2. **Never run `get_excalidraw_urls.py` before `validate_excalidraw.py` exits 0**
3. **Never write source files to the user's workspace without being asked**
4. **Always write `.animated.svg` to the user's workspace** (it is the video deliverable)
5. **Never skip or reorder the 3 steps** — even if video was the original request

## Testing

```bash
cd scripts
uv run pytest                   # full test suite
uv run pytest -m "not slow"     # skip Playwright/Chromium browser tests
```

## References

- `references/index.md` — index of all reference documents
- `references/activation-routing.xml` — full routing rules
- `references/fundamental-shapes.md` — shape vocabulary
- `references/json-schema.md` — `.excalidraw` JSON format
- `references/element-templates.md` — grid layout + element templates
- `references/animation-spec.md` — animation story patterns
- `references/quality-checklist.md` — diagram quality criteria
