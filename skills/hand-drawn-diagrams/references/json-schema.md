# Excalidraw JSON Schema

This reference focuses on the subset most useful for this skill while noting the modern fields you may see in current Excalidraw files.

## File Wrapper

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {},
  "files": {}
}
```

| Property | Description |
|----------|-------------|
| `type` | Always `excalidraw` |
| `version` | File format version |
| `source` | Usually `https://excalidraw.com` |
| `elements` | Array of scene elements |
| `appState` | Export/view settings such as background color and grid |
| `files` | Binary file map used for image-backed elements |

## Element Types

| Type | Use For |
|------|---------|
| `rectangle` | Processes, actions, components |
| `ellipse` | Entry/exit points, external systems |
| `diamond` | Decisions, conditionals |
| `arrow` | Connections between shapes |
| `text` | Labels inside shapes |
| `line` | Non-arrow connections |
| `frame` | Grouping containers |

The broader Excalidraw schema also includes types such as `freedraw`, `image`, `embeddable`, `iframe`, and `magicframe`. This skill normally avoids those unless the user explicitly needs them.

## Common Properties

All elements share these:

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `type` | string | Element type |
| `x`, `y` | number | Position in pixels |
| `width`, `height` | number | Size in pixels |
| `strokeColor` | string | Border color (hex) |
| `backgroundColor` | string | Fill color (hex or "transparent") |
| `fillStyle` | string | "solid", "hachure", "cross-hatch" |
| `strokeWidth` | number | 1, 2, or 4 |
| `strokeStyle` | string | "solid", "dashed", "dotted" |
| `roughness` | number | 0 (smooth), 1 (default), 2 (rough) |
| `opacity` | number | 0-100 |
| `seed` | number | Random seed for roughness |
| `version` | number | Incremented on edit |
| `versionNonce` | number | Additional reconciliation nonce |
| `index` | string or null | Fractional ordering metadata |
| `groupIds` | array | Nested group membership |
| `frameId` | string or null | Parent frame, if grouped in a frame |
| `boundElements` | array or null | Bound text/arrows metadata |
| `updated` | number | Last updated epoch ms |
| `link` | string or null | Optional hyperlink |
| `locked` | boolean | Whether the element is locked |
| `isDeleted` | boolean | Soft deletion flag |
| `customData` | object | Optional app-specific metadata |

## Text-Specific Properties

| Property | Description |
|----------|-------------|
| `text` | The display text |
| `originalText` | Same as text |
| `fontSize` | Size in pixels (16-20 recommended) |
| `fontFamily` | 1 for Virgil handwritten (use this) |
| `textAlign` | "left", "center", "right" |
| `verticalAlign` | "top", "middle", "bottom" |
| `containerId` | ID of parent shape |
| `lineHeight` | Unitless line height |
| `autoResize` | Whether text resizes automatically |

For hand-authored diagrams:
- `originalText` should preserve the clean source string.
- `text` may be wrapped by Excalidraw for bound/container text.
- Bound text inside shapes and arrows usually works best with `autoResize: true`.
- Fixed `width`/`height` guesses are a common source of clipped text.

## Arrow-Specific Properties

| Property | Description |
|----------|-------------|
| `points` | Array of [x, y] coordinates |
| `startBinding` | Connection to start shape |
| `endBinding` | Connection to end shape |
| `startArrowhead` | null or an arrowhead type |
| `endArrowhead` | null or an arrowhead type |
| `elbowed` | Optional orthogonal routing mode |

Common arrowheads in current Excalidraw include `arrow`, `bar`, `dot`, `triangle`, `triangle_outline`, `diamond`, `diamond_outline`, `circle`, and `circle_outline`.

Arrow labels are represented as `text` elements whose `containerId` points to the arrow `id`, while the arrow lists the text in `boundElements`.

## Binding Format

```json
{
  "elementId": "shapeId",
  "focus": 0,
  "gap": 2
}
```

## Modern Export Notes

- Current Excalidraw utility APIs expose both `exportToSvg()` and `exportToBlob()`.
- Scene size is effectively unbounded for authoring, but PNG/canvas export can still hit browser raster limits.
- For very large diagrams, SVG or scaled raster export is safer than assuming one huge PNG will always work.

## Rectangle Roundness

Add for rounded corners:
```json
"roundness": { "type": 3 }
```
