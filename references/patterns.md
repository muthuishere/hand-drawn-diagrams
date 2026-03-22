# Visual Pattern Library

## Fan-Out (One-to-Many)
Central element with arrows radiating to multiple targets. Use for: sources, PRDs, root causes, central hubs.
```
        ○
       ↗
  □ → ○
       ↘
        ○
```
Implementation hint: one central `ellipse` or `rectangle`, 2-6 target elements, and bound `arrow` elements radiating outward. Let arrows bow outward or bend if straight lines would cut through nodes.

## Convergence (Many-to-One)
Multiple inputs merging through arrows to single output. Use for: aggregation, funnels, synthesis.
```
  ○ ↘
  ○ → □
  ○ ↗
```
Implementation hint: multiple source nodes plus `arrow` elements converging into one destination shape. Leave enough whitespace so arrows can merge without slicing through containers.

## Tree (Hierarchy)
Parent-child branching with connecting lines and free-floating text (no boxes needed). Use for: file systems, org charts, taxonomies.
```
  label
  ├── label
  │   ├── label
  │   └── label
  └── label
```
Use `line` elements for the trunk and branches, free-floating text for labels.
Implementation hint: use `line` for the trunk/branches and free-floating `text`, avoiding boxes unless a node truly needs one.

## Spiral/Cycle (Continuous Loop)
Elements in sequence with arrow returning to start. Use for: feedback loops, iterative processes, evolution.
```
  □ → □
  ↑     ↓
  □ ← □
```
Implementation hint: use 3+ `arrow.points` for bends or curves; optional `roundness` can soften the loop. Prefer soft detours around boxes over straight cuts through them.

## Cloud (Abstract State)
Overlapping ellipses with varied sizes. Use for: context, memory, conversations, mental states.
Implementation hint: overlap 3-5 `ellipse` elements with varied scale and minimal labels.

## Assembly Line (Transformation)
Input → Process Box → Output with clear before/after. Use for: transformations, processing, conversion.
```
  ○○○ → [PROCESS] → □□□
  chaos              order
```
Implementation hint: keep the main path linear with one dominant process shape and short supporting labels.

## Side-by-Side (Comparison)
Two parallel structures with visual contrast. Use for: before/after, options, trade-offs.
Implementation hint: mirror layout left/right and use one divider `line` or whitespace gap between the sides.

## Gap/Break (Separation)
Visual whitespace or barrier between sections. Use for: phase changes, context resets, boundaries.
Implementation hint: use whitespace first, then optional dashed `line` or a light `frame` if grouping clarity is needed.

## Hero + Satellites
One central visual idea with a few supporting callouts. Use for: teaching, explainers, concept overviews.
```text
      [hero doodle]
       /   |   \
   note  note  note
```
Implementation hint: use one memorable center element such as an eye, sun, API box, or browser sketch, then 3-4 short supporting notes around it.

## Annotated Object
One sketched object with labels around it. Use for: optics, anatomy, page explanation, component breakdown.
```text
   label -> [object sketch] <- label
             ^      |
           label   label
```
Implementation hint: draw one main object with simple lines/shapes, keep labels outside the object, and use short arrows only where needed.

## Lines as Structure
Use lines (type: `line`, not arrows) as primary structural elements instead of boxes:
- **Timelines**: Vertical or horizontal line with small dots (10-20px ellipses) at intervals, free-floating labels beside each dot
- **Tree structures**: Vertical trunk line + horizontal branch lines, with free-floating text labels (no boxes needed)
- **Dividers**: Thin dashed lines to separate sections
- **Flow spines**: A central line that elements relate to, rather than connecting boxes

```
Timeline:           Tree:
  ●─── Label 1        │
  │                   ├── item
  ●─── Label 2        │   ├── sub
  │                   │   └── sub
  ●─── Label 3        └── item
```

Lines + free-floating text often creates a cleaner result than boxes + contained text.

## Arrow Routing Rule

If a straight arrow would cut through a box, bend or curve it instead.

Arrow-on-arrow crossings are acceptable. Arrow-through-box routing is usually not.

## Concept-to-Pattern Mapping

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | **Fan-out** (radial arrows from center) |
| Combines inputs into one | **Convergence** (funnel, arrows merging) |
| Has hierarchy/nesting | **Tree** (lines + free-floating text) |
| Is a sequence of steps | **Timeline** (line + dots + free-floating labels) |
| Loops or improves continuously | **Spiral/Cycle** (arrow returning to start) |
| Is an abstract state or context | **Cloud** (overlapping ellipses) |
| Transforms input to output | **Assembly line** (before → process → after) |
| Compares two things | **Side-by-side** (parallel with contrast) |
| Separates into phases | **Gap/Break** (visual separation between sections) |
| Needs one memorable concept with support | **Hero + Satellites** (central doodle + notes) |
| Is easiest to explain as one thing with labels | **Annotated Object** (object + callouts) |
