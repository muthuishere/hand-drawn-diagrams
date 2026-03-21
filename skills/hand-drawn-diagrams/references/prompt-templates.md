# Prompt Templates

Use these prompt formulas after selecting a mode from `references/activation-routing.xml`.

The node counts in brackets are **starting guidance, not hard caps**. Use as many nodes as the task requires to be complete. Every node must earn its place, but earning a place means being part of the answer — not being rare.

## Global Formula

```text
Create a hand-drawn [diagram type] for [audience/use case] that explains [topic].
Cover all key concepts needed to fully answer the question.
Use [layout direction] and pick the best visual pattern for the subject.
Keep each node distinct — no duplicate labels or decorative filler.
Route arrows through whitespace; bend or curve around boxes rather than through them.
```

## Teachers

```text
Create a hand-drawn teaching diagram that explains [topic] for [audience level].
Cover all major concepts needed to understand [topic] fully.
Use a [top-to-bottom / annotated-object / comparison / tree] layout.
Include 1 visual anchor that makes the topic memorable, 1 concrete example grounded in the real subject, and 1 takeaway.
Avoid turning every concept into the same box — use timelines, trees, or annotated objects where they fit better.
Use the user's language by default; use English only for short standard terms.
Every element must be distinct and necessary.
```

## Ideation

```text
Turn these notes into a hand-drawn ideation map.
Use a center-out layout. Cover all the clusters present in the input.
Highlight 1 promising direction clearly.
Keep each note short — bullets or short phrases only.
Make it exploratory, not polished.
```

## UX

```text
Create a hand-drawn UX flow for [journey/use case].
Use a left-to-right layout covering all screens or states in the flow.
Include failure or alternate branches where they exist and 1 success outcome.
Keep the main path visually obvious.
Route connectors around screens and boxes — not through them.
```

## Sales Funnel

```text
Create a hand-drawn sales funnel for [business/use case].
Use a top-wide to bottom-narrow layout with all funnel stages.
Show major drop-off or friction points and the clear conversion target.
Keep metrics sparse and readable.
```

## Technical Explainer

```text
Create a hand-drawn technical explainer diagram for [architecture/API/protocol question].
Use [left-to-right / top-to-bottom] layout covering all primary nodes needed to answer the question.
Include 1 clear flow spine, 1 visual anchor (browser sketch, database cue, etc.), failure branches where they exist, and at least 1 concrete evidence artifact (JSON payload, event name, etc.).
Use real technical names where they matter.
Route arrows around services, databases, and evidence panels; arrow-on-arrow crossings are acceptable.
Do not collapse into a generic row of equal boxes.
```

## Medical

```text
Create a hand-drawn medical explainer diagram for [condition/process/question].
Use [top-to-bottom / left-to-right] layout covering all major steps, states, and decision points.
Include all visible decision or action points and 1 patient-facing takeaway.
Prefer plain-language labels unless the audience is expert.
```

## Page Mockup

```text
Create a hand-drawn page mockup for [page type/product].
Use a top-to-bottom webpage layout covering all sections of the page.
Keep the sketch font, strong hierarchy, and 1 clear primary CTA.
If color is used, limit to 1-2 accent colors for UX emphasis only.
Only use arrows for annotations or flow overlays; keep them outside major content blocks.
```

## Wireframe

```text
Create a hand-drawn wireframe for [page/flow].
Use a [top-to-bottom / left-to-right] layout covering all sections or states.
Keep the sketch font and rough visual style.
Prefer monochrome with minimal accent only if needed for clarity.
Focus on hierarchy, layout, and CTA placement rather than decoration.
Route connectors around screens and boxes — not through them.
```

## Comparison Template

```text
Create a hand-drawn comparison diagram for [A] vs [B].
Use a side-by-side layout covering all meaningful comparison points.
Keep the visual weight on the key differences.
Include 1 bottom-line takeaway.
```

## Failure / Retry Template

```text
Create a hand-drawn flow diagram for [system/process].
Show the normal path first, then all visible failure branches, then recovery or retry paths.
Mark each decision point clearly.
Prefer a visible spine with short side arrows over one long diagonal connector through multiple boxes.
```

## Dense Input Template

```text
Convert this raw input into a hand-drawn diagram:
[paste notes]

Choose the best mode automatically.
Cover all concepts present in the input — do not drop content to reduce node count.
Keep each element distinct and necessary.
Preserve the sketch font and hand-drawn style.
```
