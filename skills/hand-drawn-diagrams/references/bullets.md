# Bullet Lists (Hand-Drawn Style)

Keep bullets readable, short, and aligned. Use the same sketch font (fontFamily: 1) and avoid cramming paragraphs into one list.

## How to Build

- Use a single `text` element with line breaks for the list when possible.
- Keep `autoResize: true`.
- Left align (`textAlign: "left"`), `lineHeight: 1.25`.
- Use a simple glyph: `•` or `-` (preferred: `•`).
- Limit line length so it does not wrap awkwardly; expand the container instead of squeezing text.
- One list per container; avoid scattering bullets across multiple boxes.

## Spacing

- One blank space after the bullet glyph.
- Consistent indentation for wrapped lines (visually align with the text start).
- Vertical spacing: rely on line height; do not add manual blank lines unless separating sections.

## When to Use a Container

- Use a container only if the bullets represent one panel/section.
- If using a container:
  - bind the text with `containerId`
  - include the text id in the container `boundElements`
  - size the container so no bullets clip or overflow

## Keep It Short

- Prefer 3–7 bullets per list.
- Each bullet should carry one idea.
- If a bullet is long, split into two bullets or a short sub-line (indented) rather than a long sentence.

## Do Not

- Do not mix multiple bullet styles in one list.
- Do not center bullets.
- Do not leave bullets half-wrapped outside the box; grow the box instead.
- Do not repeat long text across multiple bullet lists.
