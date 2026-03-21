# Quality Checklist

Run through this before delivering any diagram.

## Rule Zero: Completeness

The diagram must fully answer the question the user asked. Check this first.

- **Task answered**: Does the diagram cover everything the user asked for?
- **No missing content**: Are all key concepts, steps, or components present?
- **No artificial cuts**: Were elements removed just to reduce node count rather than because they were unnecessary?

If any of these fail, go back and add the missing content before checking anything else.

---

## Validation (Run the script — do not skip)

```bash
cd {skill-root}/scripts
uv run python validate_excalidraw.py "/absolute/path/to/file.excalidraw"
```

The script checks:
- Elements array is non-empty
- All IDs are unique
- No `isDeleted: true` elements
- All `containerId` references resolve
- All `boundElements` references resolve
- All `startBinding` / `endBinding` references resolve
- No stacked elements (coordinate collision)
- No off-canvas elements
- No text overflow

Fix every error it reports before continuing.

---

## Depth & Evidence (For Technical Diagrams)
1. **Research done**: Looked up actual specs, formats, event names?
2. **Evidence artifacts**: Code snippets, JSON examples, or real data included where useful?
3. **Concrete over abstract**: Real content shown, not just labeled boxes?
4. **Educational value**: Could someone learn something concrete from this?

## Conceptual
5. **Argument**: Does the diagram SHOW something text alone couldn't?
6. **Each element distinct**: No duplicate labels — same concept not repeated in two boxes
7. **No uniform containers**: Avoided card grids of equal boxes where a timeline, tree, or annotated object would fit better?
8. **Isomorphism**: Does each visual structure mirror its concept's behavior?

## Container Discipline
9. **Minimal containers**: Could any boxed element work as free-floating text instead?
10. **Lines as structure**: Are tree/timeline patterns using lines + text rather than boxes?
11. **Typography hierarchy**: Are font size and weight creating visual hierarchy (reducing need for boxes)?

## Structural
12. **Connections**: Every relationship has an arrow or line
13. **Flow**: Clear visual path for the eye to follow
14. **Hierarchy**: Important elements are larger or more isolated
15. **No orphans**: No element is disconnected from the rest of the diagram without intent

## Technical
16–28. **Run `validate_excalidraw.py`** — it checks all of these automatically: font family, roughness, unique IDs, binding refs, container refs, text overflow, monochrome style. Fix every reported error before continuing.

Extra checks not covered by the script:
- **Frame usage deliberate**: Frames group sections, not individual elements
- **Bound text uses autoResize**: Container text and arrow labels keep `autoResize: true`

## Layout
29–33. **Run `validate_excalidraw.py`** — it checks coordinate collisions, off-canvas elements, and spread. Also verify mentally:
- Each top-level element is at a distinct grid cell
- No overcrowded regions; consistent spacing between siblings

## Visual Validation (Render when image requested)
34. **PNG rendered (if requested)**: Diagram was rendered and visually inspected when the user asked for an image
35. **No text overflow**: All text fits within its container
36. **No unintended overlaps**: Shapes and text don't overlap unless intentionally layered
37. **Arrows land correctly**: Arrows connect to intended elements without cutting through containers
38. **Arrow labels readable**: Arrow labels sit on the path cleanly and are not clipped
39. **Balanced composition**: No large empty voids or overcrowded regions
40. **Arrow routing clean**: Arrows cross other arrows rather than boxes or main labels
41. **No empty placeholders**: No empty cards, blank containers, or decorative sections
42. **No duplicated text**: Same explanatory text not repeated across multiple blocks
43. **Text is lean**: High-value words only; no filler phrases

## Delivery
44. **Source kept**: `.excalidraw` file is preserved and a hosted edit URL is provided
45. **Validation passed**: `validate_excalidraw.py` exited 0 before URL was generated
46. **Animation (if asked)**: Hosted animate URL provided when user requests animation
47. **PNG optional**: PNG export created only if the user requested an image
