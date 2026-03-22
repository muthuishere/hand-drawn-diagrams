# Technical Explainer Diagrams

Use this when the goal is to explain architecture, APIs, protocol behavior, or system flow.

Output should look like one clear system story, one visible flow spine, one memorable system anchor, and one or two concrete evidence artifacts.

Shape vocabulary: see `references/fundamental-shapes.md`.
Arrow routing: see `references/arrow-routing.md`.

## One Big Idea

One diagram should explain one technical question only.

Examples:
- How data moves
- How systems connect
- How a protocol sequence works
- Where failures or retries happen

## Best Default Layout

Default flow: left-to-right for architecture, top-to-bottom for protocol sequence

Architecture skeleton:
```text
[Actor] -> [System] -> [Service] -> [Output]
```

Protocol skeleton:
```text
[Trigger]
   |
[Step]
   |
[Step]
   |
[Result]
```

Reveal order:
1. Trigger or actor
2. Main flow spine
3. Internal systems or stages
4. Result, failure, or output

Preferred visual patterns:
- `Assembly line` for request or data transformation
- `Hero + Satellites` for system overview
- `Annotated Object` for one service, API boundary, or browser/app surface
- `Timeline` for protocols and event sequences

Do not default to a plain row of containers if one sketched object, one boundary, or one main spine would explain the system better.

## Must Show

- 1 main system story
- 3-6 primary nodes max
- 1 visual anchor such as a client sketch, service boundary, database cue, or browser/app surface
- 1 clear data or event path
- 1-2 evidence artifacts only
- real method names, payload names, or event names when technical detail matters

## Never Draw

- vendor-logo collages
- every subsystem in the company
- arrows going both directions without explanation
- architecture made only of equal boxes with no visual hierarchy

## Canonical Recipes

### 1. Architecture path
Structure: `Actor or client sketch -> boundary -> 3-5 systems -> output`

### 2. API request/response
Structure: `Client -> endpoint -> processing -> response`

### 3. Protocol sequence
Structure: `Trigger -> ordered events -> state/result`

### 4. Failure and retry path
Structure: `Normal path + one visible failure branch + one retry or recovery path`

Use comparison when possible. `Request vs response`, `before vs after transform`, and `success vs failure` are usually clearer than giant system maps.
Use small sketch cues when they help recognition: browser window, phone, queue stack, database cylinder, cloud, lock, or warning burst.

## Fundamental Shape Mapping

- `ellipse`: actor, input, trigger, external system, output
- `rectangle`: service, processor, queue stage, transformation step
- `diamond`: route, validation, authorization, retry/no-retry decision
- `arrow`: movement of data, events, control, or responsibility
- `line`: protocol timeline spine
- `frame`: section for client, backend, storage, or external region

Arrow rule:
- prefer hand-drawn bends or curves around services and data stores
- allow arrow-on-arrow crossings if needed
- avoid arrow-through-box routing

## Hard Limits

- Primary nodes: 3-6
- Major sections: 2-4
- Evidence artifacts: 1-2
- Decision diamonds: 2 max unless the whole point is branching
- Annotations: 4 max

## Evidence Artifact Rules

Use small, monochrome artifacts only:
- one JSON payload
- one API call signature
- one event list
- one state transition note

If there are more than two, split the diagram into panels.

## Bad vs Better Prompt

Bad:
"Make a hand-drawn architecture diagram for our API."

Better:
"Create a hand-drawn technical explainer diagram showing how a request moves from a browser to API to worker to database, using 1 browser sketch as the visual anchor, 4 primary nodes, 1 failure branch, and 1 real JSON payload example."

## Cut Ruthlessly

Remove in this order:
1. secondary systems
2. duplicate arrows
3. extra evidence panels

## Minimum Viable Output

- 1 trigger or actor
- 1 visual anchor
- 3 system nodes
- 1 clear flow
- 1 evidence artifact

## Acceptance Check

- Can an engineer explain the flow in under 30 seconds?
- Is the main path visually obvious before reading the small text?
- Is there enough visual hierarchy that it does not read like a generic flowchart?
- Are real technical names used where they matter?
- Is the detail level narrow enough to answer one question well?
