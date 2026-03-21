# Element Templates

Copy-paste JSON templates for each Excalidraw element type. **All elements use black stroke (#1e1e1e) with white/transparent fills** for a simple hand-drawn aesthetic.

These are safe hand-authored starting points, not a full dump of every property Excalidraw may serialize.

## Canvas Layout Grid

Canvas: 1400 × 900px. Pick a unique cell per top-level element. Do not compute — read x,y directly from this table:

```
       col1  col2  col3  col4  col5
row1   80,80  360,80  640,80  920,80  1200,80
row2   80,200  360,200  640,200  920,200  1200,200
row3   80,320  360,320  640,320  920,320  1200,320
row4   80,440  360,440  640,440  920,440  1200,440
row5   80,560  360,560  640,560  920,560  1200,560
row6   80,680  360,680  640,680  920,680  1200,680
row7   80,800  360,800  640,800  920,800  1200,800
```

Arrow x,y: start at `source.x + source.width + 2`, end at `target.x - 2`. Vertical: `source.y + source.height + 2`.

Rules:
- Bound text inherits its container's cell — do not assign it a separate cell.
- If you need more than 35 cells, shrink element sizes and shift values accordingly.
- Seeds: use distinct integers. Simple strategy: first element seed=10001, increment by 1 per element.

## Free-Floating Text (no container)
```json
{
  "type": "text",
  "id": "label1",
  "x": 100, "y": 100,
  "width": 200, "height": 25,
  "text": "Section Title",
  "originalText": "Section Title",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 11111,
  "version": 1,
  "versionNonce": 22222,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "containerId": null,
  "autoResize": true,
  "lineHeight": 1.25
}
```

## Line (structural, not arrow)
```json
{
  "type": "line",
  "id": "line1",
  "x": 100, "y": 100,
  "width": 0, "height": 200,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 44444,
  "version": 1,
  "versionNonce": 55555,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 200]]
}
```

## Small Marker Dot
```json
{
  "type": "ellipse",
  "id": "dot1",
  "x": 94, "y": 94,
  "width": 12, "height": 12,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#1e1e1e",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 66666,
  "version": 1,
  "versionNonce": 77777,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

## Rectangle
```json
{
  "type": "rectangle",
  "id": "elem1",
  "x": 100, "y": 100, "width": 180, "height": 90,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#ffffff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 12345,
  "version": 1,
  "versionNonce": 67890,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [{"id": "text1", "type": "text"}],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

## Text (centered in shape)
```json
{
  "type": "text",
  "id": "text1",
  "x": 130, "y": 132,
  "width": 120, "height": 25,
  "text": "Process",
  "originalText": "Process",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 11111,
  "version": 1,
  "versionNonce": 22222,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "containerId": "elem1",
  "autoResize": true,
  "lineHeight": 1.25
}
```

## Arrow
```json
{
  "type": "arrow",
  "id": "arrow1",
  "x": 282, "y": 145, "width": 118, "height": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 33333,
  "version": 1,
  "versionNonce": 44444,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [118, 0]],
  "startBinding": {"elementId": "elem1", "focus": 0, "gap": 2},
  "endBinding": {"elementId": "elem2", "focus": 0, "gap": 2},
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

Use this only when the path stays mostly in whitespace.

Arrow routing notes:
- Prefer edge-to-edge bindings, not center-to-center diagonals.
- If a straight path would cut through a box, switch to a bent or curved arrow.
- Arrow-on-arrow crossings are acceptable. Arrow-through-box routing is not a good default.

## Bent Arrow Around A Container
```json
{
  "type": "arrow",
  "id": "arrowBent1",
  "x": 282, "y": 145, "width": 198, "height": 120,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 33335,
  "version": 1,
  "versionNonce": 44446,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [60, 0], [60, 90], [198, 120]],
  "startBinding": {"elementId": "elem1", "focus": 0.15, "gap": 2},
  "endBinding": {"elementId": "elem2", "focus": -0.2, "gap": 2},
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

Use this when the direct line would run through an intermediate box or dense label area.

## Curved Arrow
```json
{
  "type": "arrow",
  "id": "arrowCurve1",
  "x": 280, "y": 140, "width": 180, "height": 80,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 33334,
  "version": 1,
  "versionNonce": 44445,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [90, -40], [180, 40]],
  "startBinding": {"elementId": "elem1", "focus": 0, "gap": 2},
  "endBinding": {"elementId": "elem2", "focus": 0, "gap": 2},
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

For curves: use 3+ points in `points` array and keep the detour broad enough to read in one glance.

## Frame (section grouping only)
```json
{
  "type": "frame",
  "id": "frame1",
  "x": 60, "y": 60, "width": 520, "height": 280,
  "strokeColor": "#bbbbbb",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 88888,
  "version": 1,
  "versionNonce": 99999,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "name": "Section",
  "frameId": null
}
```

## Section Title + Divider
```json
[
  {
    "type": "text",
    "id": "sectionTitle1",
    "x": 80, "y": 70,
    "width": 220, "height": 25,
    "text": "Section Title",
    "originalText": "Section Title",
    "fontSize": 20,
    "fontFamily": 1,
    "textAlign": "left",
    "verticalAlign": "top",
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 10001,
    "version": 1,
    "versionNonce": 10002,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": null,
    "link": null,
    "locked": false,
    "containerId": null,
    "lineHeight": 1.25
  },
  {
    "type": "line",
    "id": "sectionDivider1",
    "x": 80, "y": 104,
    "width": 220, "height": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "dashed",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 10003,
    "version": 1,
    "versionNonce": 10004,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": null,
    "link": null,
    "locked": false,
    "points": [[0, 0], [220, 0]]
  }
]
```

## Bound Container Pair
```json
[
  {
    "type": "rectangle",
    "id": "container1",
    "x": 100, "y": 100, "width": 220, "height": 100,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "#ffffff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 12346,
    "version": 1,
    "versionNonce": 67891,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": [{"id": "containerText1", "type": "text"}],
    "link": null,
    "locked": false,
    "roundness": {"type": 3}
  },
  {
    "type": "text",
    "id": "containerText1",
    "x": 210, "y": 150,
    "width": 168, "height": 44,
    "text": "Bound text block",
    "originalText": "Bound text block",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 11112,
    "version": 1,
    "versionNonce": 22223,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": null,
    "link": null,
    "locked": false,
    "containerId": "container1",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

Notes:
- Keep `originalText` as the clean source string.
- Keep `autoResize: true` for bound text.
- Treat the text `width`, `height`, `x`, and `y` as starter values only; Excalidraw may recompute them when rendered or edited.

## Multi-Line Text Block
```json
{
  "type": "text",
  "id": "textMulti1",
  "x": 100, "y": 100,
  "width": 240, "height": 72,
  "text": "Line one\nLine two\nLine three",
  "originalText": "Line one\nLine two\nLine three",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "seed": 12121,
  "version": 1,
  "versionNonce": 23232,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "containerId": null,
  "autoResize": true,
  "lineHeight": 1.25
}
```

## Arrow With Label
```json
[
  {
    "type": "arrow",
    "id": "arrowLabel1",
    "x": 280, "y": 140, "width": 180, "height": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 45551,
    "version": 1,
    "versionNonce": 45552,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": [{"id": "arrowLabelText1", "type": "text"}],
    "link": null,
    "locked": false,
    "points": [[0, 0], [180, 0]],
    "startBinding": {"elementId": "elem1", "fixedPoint": [1, 0.5], "mode": "inside"},
    "endBinding": {"elementId": "elem2", "fixedPoint": [0, 0.5], "mode": "inside"},
    "startArrowhead": null,
    "endArrowhead": "arrow",
    "elbowed": false
  },
  {
    "type": "text",
    "id": "arrowLabelText1",
    "x": 340, "y": 122,
    "width": 70, "height": 20,
    "text": "Label",
    "originalText": "Label",
    "fontSize": 16,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "angle": 0,
    "seed": 45553,
    "version": 1,
    "versionNonce": 45554,
    "isDeleted": false,
    "groupIds": [],
    "boundElements": null,
    "link": null,
    "locked": false,
    "containerId": "arrowLabel1",
    "autoResize": true,
    "lineHeight": 1.25
  }
]
```

Arrow label notes:
- The label is bound text on the arrow via `containerId`.
- The arrow must include the text element in `boundElements`.
- Keep `autoResize: true`.
- If the label makes a clean route messy, move or shorten the label before forcing the arrow through a box.
- Do not hand-position long arrow labels too tightly. Excalidraw calculates final placement from the arrow path.
