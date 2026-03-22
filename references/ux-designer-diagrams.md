# UX Designer Diagrams

Use this when the goal is to explain screens, user flow, navigation, or interaction logic.

Output should look like one dominant path, a small number of screens or states, and one visible success outcome.

Shape vocabulary: see `references/fundamental-shapes.md`.

## One Big Idea

One diagram should explain one journey, not the whole product.

## Best Default Layout

Default flow: left-to-right

```text
[Entry] -> [Screen] -> [Decision] -> [Success]
                 \
                 [Failure]
```

Reveal order:
1. Entry point
2. Main path
3. Branch or failure state
4. Success outcome

## Must Show

- 1 main path
- 3-5 primary screens or states
- 1 failure or alternate branch if it matters
- 1 clear end state

## Never Draw

- page layouts detailed like real UI comps
- too many annotations inside screens
- flows where the error state is missing

## Canonical Recipes

### 1. Wireflow
Structure: `Entry -> 3-5 screens -> 1 branch -> success`

### 2. Sitemap sketch
Structure: `Homepage -> primary sections -> 1 deeper level only`

### 3. Before/after UX comparison
Structure: `Current flow | Improved flow -> one visible simplification`

Use comparison when possible. `Current vs improved` often explains UX more simply than one giant flowchart.

## Hard Limits

- Screens/states: 3-5
- Branches from main path: 1-2
- annotations per screen: 2 max
- primary arrows: keep one dominant direction

## Bad vs Better Prompt

Bad:
"Create a UX flow for signup."

Better:
"Create a hand-drawn wireflow for signup with 4 screens, 1 failure branch, and 1 success state, using a left-to-right layout."

## Cut Ruthlessly

Remove in this order:
1. detailed UI chrome
2. minor notes inside screens
3. low-value branches

## Minimum Viable Output

- 1 entry point
- 3 screens
- 1 decision or branch
- 1 success state

## Acceptance Check

- Is the main user path obvious before reading all labels?
- Are screens distinct without excessive detail?
- Is the failure branch visible if it matters?
- Does the diagram end in a clear outcome?
