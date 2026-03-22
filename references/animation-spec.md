# Animation Spec

Read this before writing a `.animationinfo.json` file.

This reference covers everything `excalidraw-animate` can do and how to make the LLM-authored animation tell a clear story.

---

## What animateSvg Does Per Element Type

Each Excalidraw element type animates differently. Know this before assigning durations.

| Element Type | Animation Behaviour | Notes |
|---|---|---|
| `rectangle` | Border draws itself as a polygon, then fill fades in (75% / 25% split) | Fast border + fill looks good at 400–600ms |
| `diamond` | Same as rectangle — polygon draw + fill | |
| `ellipse` | Outline traces the oval, then fill fades in | |
| `arrow` | Shaft draws first (60% of duration), then arrowhead paths animate | Give arrows slightly more time than boxes |
| `line` | Draws along its path from start to end | Fast at 200–300ms |
| `text` | Reveals left-to-right along a sliding path clip | Short text: 200ms. Long labels: 400ms |
| `freedraw` | Interpolates stroke points one by one | |
| `image` | Opacity fade-in only — no path animation possible | 300ms fade is enough |

---

## Duration Rules

### Global defaults (when no duration specified)
- Individual ungrouped element: `500ms`
- Grouped elements total: `5000ms` divided equally among group members

### Recommended ranges
- Short label / title text: `200–300ms`
- Box or ellipse: `400–600ms`
- Arrow: `400–700ms`
- Section header: `300ms`
- Complex grouped region: `800–1200ms` total

### Total animation time
- Aim for the full diagram to finish in **8–20 seconds** for most diagrams.
- For dense diagrams (15+ elements): use `defaultDuration: 300` and group related elements.
- For simple diagrams (5–8 elements): use `defaultDuration: 500`.

---

## Order Rules

`order` controls when an element animates relative to others.

- Elements with the same `order` value animate **simultaneously**.
- Elements with lower `order` animate first.
- `order: 1` is the first thing to appear.
- Elements not listed in `elements[]` animate in their array creation order after all listed elements.

### Key ordering principles
- **Titles and headings animate first** (order 1).
- **Containers before their content** — the box draws before the text inside.
- **Arrows after their source and target** — never animate an arrow before the boxes it connects.
- **Group related elements at the same order** — a container and its bound text should share an order so they appear together.
- **Don't give every element a unique order** unless you want strictly sequential (adds time). Siblings at the same level should share an order.

---

## animationinfo.json Format

```json
{
  "startMs": 500,
  "defaultDuration": 500,
  "elements": [
    { "id": "elem-id-1", "order": 1, "duration": 300 },
    { "id": "elem-id-2", "order": 1, "duration": 300 },
    { "id": "elem-id-3", "order": 2, "duration": 500 },
    { "id": "arrow-1",   "order": 3, "duration": 400 }
  ]
}
```

| Field | Default | Description |
|---|---|---|
| `startMs` | `500` | Pause before animation begins (ms) |
| `defaultDuration` | `500` | Duration for any element not listed in `elements` |
| `elements[].id` | required | The exact element id from the `.excalidraw` file |
| `elements[].order` | `0` | Sequence position — lower = earlier |
| `elements[].duration` | `defaultDuration` | How long this element takes to draw (ms) |

**Use an array, not an object map.** The array narrates the story in sequence — the LLM writes it top-to-bottom in the order the story should unfold.

---

## Story Patterns

Pick one pattern and apply it to the full diagram. Do not mix patterns within the same diagram.

### `reveal-top-down`
Best for: flows, sequences, step-by-step processes.

Assign `order: 1` to the topmost row, `order: 2` to the next, and so on. Containers and their bound text share the same order. Arrows between rows get the order of the row they point *to*.

```
title               order: 1
step-1-box          order: 2
step-1-text         order: 2
arrow-1→2           order: 3
step-2-box          order: 3
step-2-text         order: 3
arrow-2→3           order: 4
step-3-box          order: 4
step-3-text         order: 4
```

### `context-first`
Best for: architecture diagrams, system maps, infrastructure diagrams.

Outer frame or context boundary first, then inner services, then arrows connecting them.

```
outer-frame         order: 1
service-a-box       order: 2
service-a-text      order: 2
service-b-box       order: 2
service-b-text      order: 2
arrow-a→b           order: 3
arrow-b→c           order: 3
```

### `problem-solution`
Best for: teaching diagrams, before/after, explainers.

The problem or question appears first. The solution or answer builds afterward.

```
question-title      order: 1
problem-box         order: 2
arrow-to-solution   order: 3
solution-box        order: 4
solution-text       order: 4
takeaway            order: 5
```

### `build-left-right`
Best for: pipeline diagrams, data flow, assembly lines.

Each stage (box + label) animates together, sweeping left to right. Arrows between stages animate with the stage they connect to.

```
stage-1-box         order: 1
stage-1-label       order: 1
arrow-1→2           order: 2
stage-2-box         order: 2
stage-2-label       order: 2
arrow-2→3           order: 3
stage-3-box         order: 3
stage-3-label       order: 3
```

### `simultaneous-groups`
Best for: side-by-side comparisons, two-column layouts.

Both columns animate in parallel row by row — same `order` values on left and right.

```
left-title          order: 1
right-title         order: 1
left-row1           order: 2
right-row1          order: 2
left-row2           order: 3
right-row2          order: 3
divider-line        order: 1
```

---

## What Not To Do

- **Don't set order:0 on everything** — that degenerates to default array order with no story.
- **Don't give 20 elements 20 unique orders** — a 20-element diagram at 500ms each = 10+ seconds of waiting.
- **Don't animate arrows before their connected boxes** — it looks broken.
- **Don't separate a container from its bound text** — they should share the same order.
- **Don't use durations under 150ms** — too fast to perceive the draw effect.
- **Don't use durations over 2000ms per element** — becomes painfully slow.

---

## Writing animationinfo.json — Checklist

Before writing the file:
1. Choose one story pattern that fits the diagram layout.
2. **Only list elements that need a specific order or non-default duration.** Unlisted elements animate in source-array order at `defaultDuration` — do not enumerate every element.
3. Group container + bound text pairs at the same order.
4. Put arrows after the shapes they connect.
5. Choose `defaultDuration` based on diagram density (300 for dense, 500 for normal).
6. Check total time: number of sequential order groups × avg duration should be 8–20s.
7. Write the array in story order — top of array = first to appear.
