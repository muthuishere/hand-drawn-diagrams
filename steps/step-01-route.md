# Step 01: Route

Pick the smallest matching route from `references/activation-routing.xml`.

Default route selection:
- `teachers`: teach, explain simply, lesson, compare, ELI5
- `ideation`: brainstorm, cluster notes, opportunity map, organize thinking
- `ux`: journey, wireflow, sitemap, screen flow, product flow
- `sales-funnel`: funnel, drop-off, conversion, leads, qualification
- `technical-explainer`: architecture, API, protocol, event flow, integration, failure/retry
- `medical`: condition, diagnosis, treatment, patient explanation
- `creative-raw`: explicit full creative mode, open composition, pick any diagram style that fits best
- `page-mockup`: webpage, dashboard, landing page, pricing page, UI mockup

Selection rule:
- choose one primary route
- borrow one secondary reference only if it clearly improves the result without widening scope

Load first:
- `references/activation-routing.xml`
- `references/fundamental-shapes.md`

Then load one route guide:
- `references/teachers-diagrams.md`
- `references/ideation-diagrams.md`
- `references/ux-designer-diagrams.md`
- `references/sales-funnel-diagrams.md`
- `references/technical-explainer-diagrams.md`
- `references/medical-diagrams.md`
- `references/creative-raw-diagrams.md`
- `references/page-mockup-diagrams.md`

If the ask is technical or factual:
- research real names, payloads, states, or steps before drawing

Always:
- make one diagram answer one main question
- prefer the smallest useful structure
- do not use many references at once
- if the user's topic is broad (covers multiple concepts), pick the single most important one; note the others as possible follow-up diagrams rather than trying to fit everything into one diagram

## Delivery mode — set this before drawing

Read the user's request and infer the **open mode** for `open_diagram.py`:

| What user asked for | `--mode` to pass | What happens |
|---|---|---|
| just a diagram / default / "show me" / "open" | `edit` | Redirect to hosted Excalidraw editor |
| "watch it animate" / "open animation" / "show animation" | `animate` | Redirect to hosted animation view |
| "save the file" / "save as excalidraw" / "keep the source" | `save-excalidraw` | Copy `.excalidraw` to project |
| "animation video" / "animated SVG" / "save animation" | `save-animation` | Render + save `.animated.svg` to project |
| "save image" / "export PNG" / "save PNG" | `save-image` | Render + save `.png` to project |
| "show image" / "open image" / "open PNG" | `open-image` | Render `.png`, save it, open with system viewer |

**One mode per request.** If the user says "animate and save it", pick `save-animation` (the file is the primary ask).

**Critical order for any render mode (`save-animation`, `save-image`, `open-image`):**
1. Complete the diagram (step-02 writes the `.excalidraw` file)
2. Validate (step-03 pre-flight)
3. **Then** call `open_diagram.py` with the right mode — never before the diagram exists

Do not skip to rendering. The `.excalidraw` file must exist and validate clean first.
