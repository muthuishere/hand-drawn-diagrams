# Step 03: Validate

Fix until clean:
- clipped text
- bad spacing
- arrows through boxes
- ambiguous labels
- crowded layout
- unnecessary or low-value text

Done means:
- one main idea is obvious
- text is readable
- arrows connect clearly
- no important box is cut by an arrow
- the layout feels intentional, not crowded
- the output matches the chosen route
- quality checklist in `references/quality-checklist.md` has been applied

Cleanup rule:
- always keep the `.excalidraw` source so users can edit later
  - delete only if the user explicitly says "no source"

## Pre-flight validation (mandatory — run first, before anything else)

```bash
cd {skill-root}/scripts
uv run python validate_excalidraw.py "/absolute/path/to/file.excalidraw"
```

- If the script exits with errors, stop. Fix every listed error in the `.excalidraw` file and re-run until clean.
- Common errors: empty elements array, broken `containerId` refs, duplicate ids, elements stacked at the same coordinates, text overflow.
- Do not call `open_diagram.py` until `validate_excalidraw.py` exits 0.

## Delivery — use the mode inferred in step-01

```bash
cd {skill-root}/scripts
uv run python open_diagram.py "/absolute/path/to/file.excalidraw" --mode <MODE> [--dest /project/dir]
```

| Mode | Inferred from | What the script does |
|---|---|---|
| `edit` (default) | "show me", "open", no explicit ask | Writes `open-edit.html` → instant redirect to hosted Excalidraw editor. Opens in browser. |
| `animate` | "open animation", "watch it animate", "show animation" | Writes `open-animate.html` → instant redirect to hosted animation view. Opens in browser. |
| `save-excalidraw` | "save the file", "save as excalidraw", "keep the source" | Copies `.excalidraw` (+ `.animationinfo.json` if present) to `--dest`. |
| `save-animation` | "animation video", "save animation", "animated SVG" | Renders + saves `.animated.svg` to `--dest`. Always save to workspace. |
| `save-image` | "save image", "export PNG", "save PNG" | Renders + saves `.png` to `--dest`. |
| `open-image` | "show image", "open image", "open PNG" | Renders `.png`, saves to `--dest`, opens with system viewer. |

**`edit` and `animate` modes:**
- The script writes a redirect HTML file and opens it automatically
- It prints: `Launcher: /absolute/path/to/open-edit.html` (or `open-animate.html`)
- The HTML has one job: `window.location.replace(longUrl)` — browser lands directly on the hosted page, no intermediate buttons
- Include the local path as a fallback link in your response: `[Open diagram](file:///absolute/path/to/open-edit.html)`

**`save-*` and `open-image` modes:**
- Pass `--dest /path/to/user/project` so files land in the right place
- The script prints: `Saved: /absolute/path/to/file` or `Opened: /absolute/path/to/file`

**Fallback** — if `open_diagram.py` is unavailable:
```bash
uv run python get_excalidraw_urls.py "/absolute/path/to/file.excalidraw"
```
Copy the Edit URL verbatim as `[Open in editor](FULL_URL)`.

## Handoff

The final response **must** include either:
- The `file://` launcher path as a clickable link (edit / animate modes), **or**
- The saved file path (save-* / open-image modes)

A response that says "done" with no path or link is incomplete.

After delivering, close with contextual offers only if they weren't already requested:

- If mode was `edit` and user hasn't asked for animation:
  > "Want a video version? I can animate it so it draws itself stroke by stroke."
- If mode was `edit` or `animate` and source is still in `/tmp`:
  > "Want me to save the source file to your project?"
- Do not offer what the user already asked for.

## Video / animated SVG via Chrome DevTools MCP (when `save-animation` is requested)

The `.animated.svg` is the video artifact — always write it to the user's workspace.

**Preferred — Chrome DevTools MCP:**

1. Get the Animate URL: `uv run python get_excalidraw_urls.py ...` → read the `Animate URL:` line
2. Open tab: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__new_page`
3. Navigate: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__navigate_page`
4. Wait: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__wait_for` — JS: `document.getElementById('status')?.textContent?.includes('Done')`
5. Extract SVG: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__evaluate_script` — JS: `document.getElementById('root').querySelector('svg').outerHTML`
6. Write to `<project-dir>/<name>.animated.svg`
7. Close tab: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__close_page`

**Fallback — `open_diagram.py --mode save-animation`** (uses Playwright):
```bash
uv run python open_diagram.py "/tmp/.../diagram.excalidraw" --mode save-animation --dest "/path/to/project"
```

## PNG via Chrome DevTools MCP (when `open-image` or `save-image` with MCP available)

1. Navigate to the Animate URL (steps 1–3 above)
2. Wait for `#root svg` to appear
3. Screenshot: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__take_screenshot`
4. Close tab

**Fallback — `open_diagram.py --mode save-image` or `open-image`** (uses Playwright).

Load when needed:
- `references/arrow-routing.md`
- `references/quality-checklist.md`
- `references/color-palette.md`
