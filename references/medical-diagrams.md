# Medical Diagrams

Use this when the goal is to explain symptoms, conditions, body processes, clinical pathways, triage, treatment flow, or patient education.

Output should look like one clear pathway, one patient-relevant explanation, and one visible outcome or decision point.

Shape vocabulary: see `references/fundamental-shapes.md`.

## One Big Idea

One diagram should explain one medical question only.

Examples:
- What is happening in the body
- How symptoms progress
- How diagnosis or triage works
- What treatment sequence looks like

## Best Default Layout

Default flow: top-to-bottom for clinical pathways, left-to-right for body-process explanation

Clinical pathway skeleton:
```text
[Patient/Symptom]
      |
 [Assessment]
      |
 [Decision]
   /      \
[Path A] [Path B]
```

Body-process skeleton:
```text
[Cause] -> [Body process] -> [Symptom] -> [Action/Outcome]
```

Reveal order:
1. Patient state, symptom, or condition
2. What is happening
3. The key decision or intervention
4. The outcome or next action

## Must Show

- 1 medical question only
- 3-5 major states or steps
- 1 visible decision point if diagnosis or triage is involved
- 1 patient-facing outcome or action
- plain-language labels unless expert audience is explicit

## Never Draw

- dense textbook-style anatomy boards
- 8 competing symptom branches
- jargon-heavy labels with no patient meaning

## Canonical Recipes

### 1. Symptom to action
Structure: `Symptom -> likely cause -> what to do`

### 2. Body-process explanation
Structure: `Cause -> internal process -> symptom -> result`

### 3. Triage or diagnosis path
Structure: `Patient state -> assessment -> decision -> next path`

### 4. Treatment flow
Structure: `Condition -> intervention steps -> expected outcome`

Use comparison when possible. `Normal vs affected`, `mild vs severe`, and `before treatment vs after treatment` are often simpler than branching webs.

## Fundamental Shape Mapping

- `ellipse`: patient, symptom, state, outcome
- `rectangle`: assessment, treatment, intervention, explanatory step
- `diamond`: diagnostic gate, urgency decision, escalation choice
- `arrow`: progression, cause/effect, clinical handoff
- `frame`: optional section for symptoms, diagnosis, treatment, recovery

## Hard Limits

- Major steps or states: 3-5
- Decision diamonds: 2 max
- body regions or sub-processes: 3 max
- annotations: 4 max

## Language Rules

- Prefer everyday words first
- Add medical terms only if needed
- Keep labels short
- Use one safety-oriented action if appropriate

## Bad vs Better Prompt

Bad:
"Make a medical hand-drawn diagram about asthma."

Better:
"Create a hand-drawn medical explainer diagram that shows what happens during an asthma attack using 4 steps, 1 plain-language body-process explanation, and 1 action-oriented takeaway."

## Cut Ruthlessly

Remove in this order:
1. secondary anatomy detail
2. low-value labels
3. extra branches that do not change the main explanation

## Minimum Viable Output

- 1 symptom or condition
- 3-step process
- 1 decision or action
- 1 outcome or takeaway

## Acceptance Check

- Is the main medical story understandable in one pass?
- Does the diagram avoid unnecessary jargon?
- Is the key decision or action visible?
- Would the intended audience know what to do or understand after seeing it?
