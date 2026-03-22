---
name: hand-drawn-diagrams-workflow
---

# Hand-Drawn Diagrams Workflow

Create diagrams that are simple, readable, and useful.

`{skill-root}` = the installed root folder of this skill.
If the client exposes a built-in skill directory variable, use that equivalent.
Example: Claude Code may expose `${CLAUDE_SKILL_DIR}` for the installed skill folder.

`{project-root}` = the active project folder where the user is working.
If the client exposes a built-in project directory variable, use that equivalent.
Example: Claude Code may expose `${CLAUDE_PROJECT_DIR}` for the active project folder.

Defaults:
- hand-drawn
- same sketch font
- monochrome
- files written to system temp dir by default — do NOT litter the user's workspace
- hosted edit URL surfaced by default — always the first thing delivered
- PNG only if the user explicitly asks; use Chrome DevTools MCP (fast, no install)
- animated SVG only if user asks or confirms the offer

File location rule:
- `.excalidraw` + `.animationinfo.json` → `/tmp/hand-drawn-diagrams/<name>/` by default (temp, not workspace)
- Only write source to workspace if user specifies a path or explicitly asks to save it
- `.animated.svg` → **always** written to the user's workspace — it is the video deliverable
- After delivering the URL, offer to save the source if it's in temp

Default handoff pattern (fast path first, everything else opt-in):
1. Run `open_diagram.py` — writes `open.html` alongside the diagram and opens it in the browser. Deliver the local `file://` path as a clickable link. Do not paste the raw hosted URL (it is too long to be useful).
2. Offer animation: "Want a video version? I can render it as an animated diagram that draws itself (~10s)"
3. If user wants a PNG image: use Chrome DevTools MCP to screenshot the animate URL — fast, no Playwright
4. Run `render_animated_svg.py` only if Chrome DevTools MCP is unavailable

Rendering priority:
1. Chrome DevTools MCP (preferred — uses real browser, instant, no install)
2. Playwright scripts (fallback — only if MCP not available)

Exception:
- use restrained color only for page mockups when the user explicitly wants webpage-like fidelity

Process:
1. Read `./steps/step-01-route.md` — pick one route, scope to one main question
2. Read `./steps/step-02-draw.md` — design the diagram, then **write** the `.excalidraw` file with a non-empty elements array
3. Read `./steps/step-03-validate.md` — confirm file is non-empty, then run quality checklist and deliver

Critical: step-02 must write the file before step-03 runs. Never encode or share a URL for an empty file.

Animation/video order rule:
- If the user explicitly asked for a video or animation: still follow steps 1→2→3 in order
- The `.excalidraw` file must exist and validate before any rendering starts
- Never render before the diagram is drawn — not even if video was the original request

Core rule:
- activation chooses the job
- steps handle the work
- references hold the detail

Path rule:
- use relative paths such as `./steps/...` and `references/...` inside the skill
- use `{skill-root}` only when showing a command that must be run from the installed skill folder
