# Step 03: Validate

Render and inspect only when an image export is requested.

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
- if the user asked for an image, a PNG was rendered and visually inspected in this session
 - quality checklist in `references/quality-checklist.md` has been applied

Cleanup rule:
- always keep the `.excalidraw` source so users can edit later
  - delete only if the user explicitly says "no source"

Pre-flight validation (mandatory — run this first, before anything else):

```bash
cd {skill-root}/scripts
uv run python validate_excalidraw.py "/absolute/path/to/file.excalidraw"
```

- If the script exits with errors, stop. Fix every listed error in the `.excalidraw` file and re-run until clean.
- Common errors to fix: empty elements array, broken `containerId` refs, duplicate ids, elements stacked at the same coordinates, text overflow.
- Do not run `get_excalidraw_urls.py` until `validate_excalidraw.py` exits 0.

Hosted edit URL — always provide after validation passes:

```bash
cd {skill-root}/scripts
uv run python get_excalidraw_urls.py "/absolute/path/to/file.excalidraw"
```

- the script prints two lines to stdout: `Edit URL:` followed by the URL, then `Animate URL:` followed by the URL
- **read the full stdout output** — the URLs are long strings starting with `https://`
- **copy the Edit URL verbatim into your response** — do not paraphrase, do not say "see above", do not leave it blank
- format it as a clickable link: `[Open in editor](PASTE_FULL_URL_HERE)`
- if the tool output was truncated, re-run the script or read the URL from the output before continuing
- tell users they can edit in the hosted page without installing Excalidraw

## Handoff

The final response to the user **must** contain the full Edit URL as a clickable link. A response that says "Edit it here:" with no URL, or omits the URL entirely, is incomplete — do not send it.

After delivering the edit URL, always close with this offer (unless the user already requested a video):

> "Want a video version of this? I can render it as an animated diagram that draws itself — takes about 10 seconds."

If the source file was written to temp and the user might want to edit it locally:
> "Want me to save the source file to your project?"

## Video / animated SVG (always saved to workspace)

The animated `.svg` is the video artifact — it plays in any browser, no app needed. **Always write it to the user's current workspace/project directory**, not temp. It is the primary deliverable when a "video" is requested.

**Preferred — Chrome DevTools MCP (fast, uses real browser):**

1. Get the Animate URL from `get_excalidraw_urls.py` (already computed above)
2. Open a new tab: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__new_page`
3. Navigate to the Animate URL: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__navigate_page`
4. Wait for animation to finish:
   `mcp__plugin_chrome-devtools-mcp_chrome-devtools__wait_for` — JS: `document.getElementById('status')?.textContent?.includes('Done')`
5. Extract the animated SVG:
   `mcp__plugin_chrome-devtools-mcp_chrome-devtools__evaluate_script` — JS: `document.getElementById('root').querySelector('svg').outerHTML`
6. Write the result to `<project-dir>/<name>.animated.svg`
7. Close the tab: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__close_page`

**Fallback — Playwright (only if Chrome DevTools MCP unavailable):**
```bash
cd {skill-root}/scripts
uv run python render_animated_svg.py "/tmp/hand-drawn-diagrams/<name>/diagram.excalidraw" \
  --output "/path/to/project/<name>.animated.svg"
```

## PNG (only when user explicitly asks for an image)

**Preferred — Chrome DevTools MCP:**

1. Navigate to the Animate URL (steps 1–4 above, stop before extracting SVG)
2. Wait for `#root svg` to appear
3. Screenshot: `mcp__plugin_chrome-devtools-mcp_chrome-devtools__take_screenshot`
4. Close the tab

**Fallback — Playwright:**
```bash
cd {skill-root}/scripts
uv run python render_excalidraw.py "/tmp/hand-drawn-diagrams/<name>/diagram.excalidraw"
```

Video / animation offer rules:
- offer once, clearly, at the end of the handoff message
- do not offer if user already asked for a video (just run it)
- do not offer if user said "no animation" or "just the diagram"
- if the user accepts, run immediately without asking further questions
- always save the `.animated.svg` to the workspace — it is the deliverable

Load when needed:
- `references/arrow-routing.md`
- `references/quality-checklist.md`
- `references/color-palette.md`
