# Step 02: Draw

Use the shared shape language from `references/fundamental-shapes.md`.

Default shape set:
- `text`
- `rectangle`
- `ellipse`
- `diamond`
- `line`
- `arrow`
- `frame` only when section grouping helps

Load when needed:
- `references/patterns.md`
- `references/prompt-templates.md`
- `references/element-templates.md`
- `references/json-schema.md`

Draw rules:
- use the same sketch font
- headings and section titles are allowed; keep them short and visually clear
- prefer whitespace over dense packing
- bind text to containers and arrows when it belongs there
- arrows may cross other arrows
- arrows should avoid boxes, major labels, and evidence panels
- if a straight arrow cuts through content, use 3+ points and bend or curve it
- text inside a shape uses `containerId` plus matching `boundElements`
- arrow labels are bound text on the arrow
- prefer `autoResize: true` for text
- every visible container must have a real purpose and real content
- if a region becomes empty after simplification, remove it instead of leaving an empty box
- if long text repeats or wraps badly across multiple regions, shorten it or keep it in one place only
- if text overflows a container, grow the container; never force long text into a fixed small box
- group text with its container via `containerId` + `boundElements`; do not leave container text unbound
- arrows should be connected to two shapes with `startBinding` and `endBinding` when possible; avoid floating arrows with no targets
- when adding a container with text:
  - set `autoResize: true` on the text
  - bind the text to the container with `containerId`
  - add the text id to the container’s `boundElements`
  - size the container so the text fits without clipping
- when adding an arrow:
  - set `startBinding` and `endBinding` to the target element ids (and gaps) whenever possible
  - prefer bends/curves rather than cutting through boxes
  - keep labels as bound text on the arrow, not separate floating labels
- fills for differentiation are allowed rarely:
  - keep fills light/neutral so the diagram stays monochrome-friendly
  - use fills only to separate one important region (e.g., trust/alert), not for decoration
- text economy:
  - each shape label = 1–5 words max; never write sentences inside boxes
  - if you feel you need more text in a box, add another box instead
  - short bullets only — max 3 bullets per container, each ≤ 5 words
  - never write paragraphs inside shapes; that is notes, not a diagram
- color rule:
  - default is monochrome; do not use fills unless they materially improve clarity
  - if a fill is truly needed, use one light neutral tint and keep the rest monochrome
- bullet rule:
  - use short bullets; avoid wrapping lines into dense paragraphs
  - align bullets cleanly with consistent spacing
  - do not scatter bullet text; keep lists within one container or line block
- formulas:
  - keep formulas short and legible
  - if a formula is long, split into two lines with clear spacing instead of cramming

Do not:
- add visual variety for its own sake
- invent a new visual language for each domain
- route arrows through boxes if a bend or curve would be clearer
- write paragraphs, sentences, or long bullet lists inside boxes — that is notes, not a diagram
- put more than one distinct concept in a single box — use separate shapes instead

## Completeness Rule

The diagram must fully answer the user's question. Use as many elements as the task requires.

- Every element must represent a distinct, necessary concept — not decoration, not a duplicate.
- Do not cut content to reduce node count. If the topic has 12 concepts, show 12.
- Do not add filler elements just to fill space either.

## Layout Before Drawing

Before generating JSON, mentally assign each top-level shape a unique cell from the grid in `references/element-templates.md`. Look up x,y directly from the table — do not compute or write out coordinate planning in your response.

- No two elements may share the same (x, y) — verify mentally before writing.
- Arrow x,y comes from the source/target grid positions, not guesses.
- Go straight to writing the JSON once positions are assigned.

## Required Output Step

After designing the diagram you MUST produce two files:

### 1. The diagram — `diagram.excalidraw`

Build the complete `.excalidraw` JSON with a **non-empty `elements` array** following the schema in `references/json-schema.md` and templates in `references/element-templates.md`. Do not leave the file as an empty template.

**Where to write:**
- If the user specified a path → use that path exactly
- Otherwise → write to `/tmp/hand-drawn-diagrams/<slug>/diagram.excalidraw` (do NOT write to the user's workspace)
- After delivering the URL in step-03, offer to save to their project if they want it

### 2. The animation spec — `diagram.animationinfo.json`

Read `references/animation-spec.md`, then write a companion `.animationinfo.json` alongside the `.excalidraw` file.

Rules for writing animationinfo:
- Choose one story pattern from `animation-spec.md` that fits the diagram layout.
- **Only list elements that need non-default order or duration** — unlisted elements animate in source order at `defaultDuration`. Do not list every element.
- Use the **exact element IDs** from the `.excalidraw` file you just wrote.
- Group containers with their bound text at the same `order` value.
- Animate arrows **after** their source and target shapes.
- Choose `defaultDuration` based on density: 300ms for dense (15+ elements), 500ms for normal.
- Total animation time should be 8–20 seconds.

Confirm both files are written before moving to step-03.

Commands (run render only if an image export is requested):
```bash
cd {skill-root}/scripts
uv run python render_excalidraw.py "/absolute/path/to/file.excalidraw"
```

```bash
cd {skill-root}/scripts
uv run python edit_excalidraw.py "/absolute/path/to/file.excalidraw"
```

Hosted editing rule:
- do not tell users to open `.excalidraw` files at `excalidraw.com`
- use `edit_excalidraw.py` so the scene opens in the hosted editor page with the gzip/base64 scene in the URL hash
- from that editor page, users can download the edited `.excalidraw`
- from that editor page, users can click `Animate` to open the hosted animation view for the same scene
- when keeping editable source, prefer also giving the hosted edit URL so users can open it directly
