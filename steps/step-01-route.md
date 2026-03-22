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

Read the user's request and note the delivery mode:

| What user asked for | Delivery mode |
|---|---|
| just a diagram / default | `edit-url` — deliver hosted edit URL, offer video at end |
| animation / video / animated | `video` — still draw first, then render animated SVG |
| image / PNG / screenshot | `png` — still draw first, then screenshot via Chrome DevTools MCP |

**Critical order for `video` or `png` mode:**
1. Complete the diagram (step-02 writes the `.excalidraw` file)
2. Validate and get the URL (step-03)
3. **Then** render the video or PNG — never before the diagram exists

Do not skip to rendering. The `.excalidraw` file must exist and validate clean first.
