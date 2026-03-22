# Fundamental Shapes

Use this file as the shared visual grammar for all domain guides.

These shapes already exist in standard Excalidraw and should be enough for most hand-drawn diagrams.

## Core Rule

Prefer a small repeated vocabulary of shapes over inventing a new shape language for every domain.

## Standard Shape Meanings

| Excalidraw Type | Default Meaning | Use Notes |
|-----------------|-----------------|-----------|
| `text` | Label, explanation, annotation | Default choice for supporting detail |
| `rectangle` | Process, step, component, screen, stage | Best general-purpose container |
| `ellipse` | Input, output, actor, state, external force | Use when something feels softer or origin-like |
| `diamond` | Decision, branch, conditional, diagnostic gate | Use only when a true choice exists |
| `arrow` | Directed movement, causality, transition, handoff | Bind at both ends when possible; route around containers when needed |
| `line` | Divider, timeline spine, grouping structure | Use when relation is structural, not directional |
| `frame` | Section boundary, region, panel | Use for big grouping only, not every box |

## Hand-Drawn Defaults

- `strokeColor: #1e1e1e`
- `backgroundColor: #ffffff` or `transparent`
- `roughness: 1`
- `opacity: 100`
- `fontFamily: 1`

## Icon Rule

Use small hand-drawn icon cues when they improve understanding.

Examples:
- sun, eye, bulb, cloud, lock, database cylinder, phone, browser window
- tiny status marks like check, cross, spark, warning burst

These should feel like sketch doodles or emoji-like cues, not polished product icons.

Use them to:
- make a hero concept memorable
- distinguish categories quickly
- reduce repeated text labels

Do not:
- replace the whole diagram with icons
- mix multiple icon styles
- use colorful polished icon packs in monochrome modes

## Domain Mapping

### Teaching
- `ellipse`: topic or question
- `rectangle`: explanation step
- `line`: timeline or divider

### Ideation
- `ellipse`: cluster or theme
- `rectangle`: selected idea or next action
- `frame`: optional region for major groups

### UX
- `rectangle`: screen or state
- `diamond`: decision point
- `arrow`: user movement

### Funnel
- `ellipse`: source or audience
- `rectangle`: stage
- `diamond`: qualification gate

### Technical / Architecture / API / Protocol
- `ellipse`: external actor, trigger, inbound/outbound event
- `rectangle`: service, process, system boundary, data transformation
- `diamond`: routing or validation choice
- `line`: timeline spine or sequence backbone

### Medical
- `ellipse`: patient, symptom, body state, outcome
- `rectangle`: intervention, step, treatment, assessment
- `diamond`: diagnostic or triage decision
- `arrow`: progression, escalation, cause/effect

## Never Do This

- Assign a new meaning to the same shape inside one diagram
- Use diamonds for things that are not real decisions
- Use frames as decorative cards
- Put paragraphs inside rectangles when text could float outside
- Run long arrows through boxes when a bend or curve would be clearer
- Turn every idea into the same rounded box when a timeline, doodle, comparison, or floating label would teach better

## Minimum Useful Vocabulary

If the diagram gets too busy, reduce back to:
- `rectangle`
- `ellipse`
- `arrow`
- `text`

That four-part vocabulary is enough for most diagrams.
