# Teacher Diagrams

Use this when a diagram needs to help someone understand, remember, or explain a topic fast.

Output should give the student a complete, accurate picture of the topic — not a watered-down summary.

Shape vocabulary: see `references/fundamental-shapes.md`.

Language rule:
- use the user's language by default
- use short English terms only if they are the clearest classroom labels
- do not over-translate standard terms into awkward phrasing
- do not mix languages heavily inside the same diagram

## Diagram vs Notes — The Core Rule

**A diagram shows structure. Notes show content. Never confuse them.**

> If you are writing sentences or long bullet lists inside boxes, you are writing notes, not drawing a diagram. Stop.

- **Wrong**: one box with 10 bullets listing everything about a topic
- **Right**: 10 shapes, each named for one concept, connected by arrows

Each box label = 1–5 words. If you need more, split into more boxes.

## Completeness First

**The diagram must fully answer the question asked — as nodes, not as text.**

If the topic has 10 important concepts, show 10 **shapes**. If it has 3, show 3. Do not cut content to meet an arbitrary count, and do not stuff multiple concepts into one box.

The rule is: every element must earn its place as a distinct concept — not as a line of text inside another box.

## Best Default Layout

Default flow: top-to-bottom or left-to-right

```text
[Topic Title]
   |
[Main Concept / Hero]
 /     |     \
[A]   [B]   [C]   ... as many branches as the topic needs
 |
[Example]
 |
[Takeaway]
```

Reveal order:
1. The topic title
2. The main concept or structure
3. Supporting detail, each earning its place
4. A concrete example grounded in the real subject
5. A clear takeaway

Preferred visual patterns:
- `Hero + Satellites` for concept teaching
- `Annotated Object` when the topic is a thing students can picture
- `Timeline` for sequences
- `Side-by-Side` for compare/contrast
- `Tree` when hierarchy matters (e.g., taxonomy, classification)

Do not default to a row of equal boxes unless the topic is genuinely categorical.

## Must Show

- 1 clear topic title
- All major concepts needed to answer the question
- A logical visual structure the eye can follow
- At least 1 memorable visual anchor (doodle, object sketch, comparison spine)
- At least 1 concrete example grounded in real content
- 1 visible takeaway

## Element Quality Rules

Each element must:
- represent a real, distinct concept (not a rephrased duplicate)
- carry content worth showing (not decoration or filler)
- be positioned so it does not collide with another element

## Never Draw

- Duplicate labels — the same concept named twice in different boxes
- Paragraphs inside containers — bullets or short phrases only
- Arrows cutting through boxes — bend or curve around them
- Every idea as the same rounded card when a timeline, tree, or annotated object would teach better
- Decorative empty containers with no content

## Canonical Recipes

### 1. Explain a concept
Structure: `Title -> hero doodle or concept shape -> N supporting nodes -> one example -> takeaway`
(N = however many concepts the topic has)

### 2. Explain a sequence
Structure: `Title -> ordered steps (all of them) -> one "why it matters" note`

### 3. Compare two ideas
Structure: `Question -> left/right comparison with all relevant rows -> one bottom-line difference`

### 4. Explain one object or phenomenon
Structure: `Object sketch -> all relevant callouts -> one real-world example -> takeaway`

Use comparison when possible. `Before/after`, `wrong/right`, and `input/output` are simpler than many parallel concepts.
Use simple doodles when they help memory. Eye, sun, prism, leaf, atom, cloud, and magnet-style sketches are good examples.

## Layout Rules (Prevent Collisions)

Use the canvas layout grid from `references/element-templates.md`.

Place elements with explicit, non-overlapping coordinates:
- Each column starts at a fixed x offset
- Each row advances by element height + 40px gap minimum
- Never place two elements at the same (x, y)

## Quality vs Quantity

Wrong question: "how many nodes is enough?"
Right question: "does this diagram fully answer what was asked?"

If yes → ship it.
If no → add the missing content before shipping.

## Minimum Viable Output

- 1 title
- Complete coverage of the topic asked
- 1 visual anchor that makes the topic memorable
- 1 concrete example
- 1 takeaway
- All elements positioned without collision

## Acceptance Check

- Does the diagram fully answer the user's question without missing key content?
- Is every element distinct and necessary?
- Is there a visual anchor that makes the topic memorable?
- Is there at least one concrete example grounded in the real subject?
- Is the takeaway visible without reading everything?
- Do all elements fit without overlapping?
