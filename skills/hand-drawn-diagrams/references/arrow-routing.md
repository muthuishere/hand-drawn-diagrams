# Arrow Routing

Use this file whenever arrows are doing too much damage to the readability of a diagram.

## Core Rule

Arrows may cross other arrows if needed.

Arrows should not cut through boxes, major labels, or evidence panels unless there is no cleaner route.

## Preferred Behavior

- arrows leave a shape cleanly from an edge
- arrows travel through whitespace first
- arrows bend or curve around boxes
- arrows land on the nearest sensible side of the target
- arrow crossings are acceptable only when arrow-on-arrow

## Routing Priority

1. Do not cut through containers
2. Do not cut through important text
3. Prefer one or two bends over a long straight line through content
4. If a crossing is unavoidable, cross another arrow, not a box

## Best Default Styles

### Straight Arrow
Use when:
- source and target are aligned
- the path stays in whitespace

### Bent Arrow
Use when:
- a straight path would cut a box
- the arrow needs to go around a region

Technique:
- use 3+ points in `arrow.points`
- keep bends broad and readable

### Hand-Drawn Curve
Use when:
- the route should feel organic
- the diagram is dense and a rigid elbow looks too mechanical

Technique:
- use 3+ points
- allow soft detours around the container
- keep the curve simple enough to follow in one glance

## Anchor Guidance

- left-to-right flows: leave from the right edge of source, land on left edge of target
- top-to-bottom flows: leave from bottom edge of source, land on top edge of target
- if the nearest edge is blocked, use the next clean edge instead

## Never Do This

- one long diagonal arrow slicing through multiple boxes
- arrows cutting through the middle of a large container
- arrows running over dense paragraph text
- forcing perfect straightness when a bend would be clearer

## Good Simplification Tricks

- move the label, not the arrow, if the arrow path is already clean
- use a flow spine plus short local arrows instead of one giant connector
- split the diagram into panels if routing becomes impossible
- shorten arrows by moving related elements closer

## Bad vs Better

Bad:
`Service A -----------------------> Service B`
through the middle of 2 containers

Better:
Arrow exits `Service A`, bends through whitespace, then lands on the edge of `Service B`.

## Acceptance Check

- Do arrows avoid cutting through boxes?
- If arrows cross, are they mostly crossing other arrows?
- Can you trace each arrow path quickly?
- Would one bend or curve make the route cleaner?
