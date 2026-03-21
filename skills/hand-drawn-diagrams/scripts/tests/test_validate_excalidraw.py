"""Tests for validate_excalidraw.py — fast, no Playwright required."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import VALID_FILE
from validate_excalidraw import validate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(tmp_path: Path, data: dict) -> Path:
    f = tmp_path / "test.excalidraw"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f


def _rect(id_: str, x: int = 100, y: int = 100) -> dict:
    return {"id": id_, "type": "rectangle", "x": x, "y": y, "width": 120, "height": 60}


def _minimal_data(*elements) -> dict:
    return {"type": "excalidraw", "elements": list(elements), "appState": {}}


# ---------------------------------------------------------------------------
# Valid file
# ---------------------------------------------------------------------------

def test_real_file_passes():
    errors, _ = validate(VALID_FILE)
    assert errors == [], f"Unexpected errors on real diagram: {errors}"


def test_real_file_has_no_element_count_errors():
    """115-element file should pass all structural checks."""
    import json
    data = json.loads(VALID_FILE.read_text(encoding="utf-8"))
    assert len(data["elements"]) == 115
    errors, _ = validate(VALID_FILE)
    assert errors == []


# ---------------------------------------------------------------------------
# File-level errors
# ---------------------------------------------------------------------------

def test_file_not_found():
    errors, _ = validate(Path("/nonexistent/does-not-exist.excalidraw"))
    assert any("not found" in e.lower() for e in errors)


def test_invalid_json(tmp_path: Path):
    f = tmp_path / "bad.excalidraw"
    f.write_text("this is not json", encoding="utf-8")
    errors, _ = validate(f)
    assert any("invalid json" in e.lower() for e in errors)


def test_wrong_root_type(tmp_path: Path):
    data = {"type": "unknown", "elements": [_rect("a")], "appState": {}}
    errors, _ = validate(_write(tmp_path, data))
    assert any("type" in e.lower() for e in errors)


def test_missing_elements_key(tmp_path: Path):
    data = {"type": "excalidraw", "appState": {}}
    errors, _ = validate(_write(tmp_path, data))
    assert any("elements" in e.lower() for e in errors)


def test_empty_elements_array(tmp_path: Path):
    data = {"type": "excalidraw", "elements": [], "appState": {}}
    errors, _ = validate(_write(tmp_path, data))
    assert any("empty" in e.lower() for e in errors)


# ---------------------------------------------------------------------------
# Element-level errors
# ---------------------------------------------------------------------------

def test_duplicate_ids(tmp_path: Path):
    el1 = _rect("dup", x=100, y=100)
    el2 = _rect("dup", x=500, y=300)
    errors, _ = validate(_write(tmp_path, _minimal_data(el1, el2)))
    assert any("dup" in e and "2 times" in e for e in errors)


def test_deleted_element_flagged(tmp_path: Path):
    el = {**_rect("del1"), "isDeleted": True}
    el2 = _rect("el2", x=400, y=300)
    errors, _ = validate(_write(tmp_path, _minimal_data(el, el2)))
    assert any("del1" in e for e in errors)


def test_missing_required_field_y(tmp_path: Path):
    el = {"id": "el1", "type": "rectangle", "x": 100}  # missing y
    errors, _ = validate(_write(tmp_path, _minimal_data(el)))
    assert any('"y"' in e for e in errors)


def test_missing_required_field_id(tmp_path: Path):
    el = {"type": "rectangle", "x": 100, "y": 100}  # missing id
    errors, _ = validate(_write(tmp_path, _minimal_data(el)))
    assert any('"id"' in e for e in errors)


# ---------------------------------------------------------------------------
# Container / binding errors
# ---------------------------------------------------------------------------

def test_bad_container_id(tmp_path: Path):
    text_el = {
        "id": "txt1", "type": "text",
        "x": 100, "y": 100, "width": 80, "height": 20,
        "text": "hello", "containerId": "nonexistent-box",
    }
    errors, _ = validate(_write(tmp_path, _minimal_data(text_el)))
    assert any("nonexistent-box" in e for e in errors)


def test_bad_bound_elements_ref(tmp_path: Path):
    box = {**_rect("box1"), "boundElements": [{"id": "ghost-text", "type": "text"}]}
    errors, _ = validate(_write(tmp_path, _minimal_data(box)))
    assert any("ghost-text" in e for e in errors)


def test_valid_container_binding_passes(tmp_path: Path):
    box = {**_rect("box1"), "boundElements": [{"id": "txt1", "type": "text"}]}
    txt = {
        "id": "txt1", "type": "text",
        "x": 110, "y": 110, "width": 80, "height": 20,
        "text": "label", "containerId": "box1", "autoResize": True,
    }
    errors, _ = validate(_write(tmp_path, _minimal_data(box, txt)))
    assert errors == []


def test_bad_arrow_start_binding(tmp_path: Path):
    arrow = {
        "id": "arr1", "type": "arrow",
        "x": 100, "y": 100, "width": 100, "height": 0,
        "points": [[0, 0], [100, 0]],
        "startBinding": {"elementId": "missing-shape", "gap": 5, "focus": 0},
        "endBinding": None,
    }
    errors, _ = validate(_write(tmp_path, _minimal_data(arrow)))
    assert any("missing-shape" in e for e in errors)


def test_arrow_binding_to_existing_element_passes(tmp_path: Path):
    box = _rect("box1", x=80, y=80)
    arrow = {
        "id": "arr1", "type": "arrow",
        "x": 200, "y": 130, "width": 100, "height": 0,
        "points": [[0, 0], [100, 0]],
        "startBinding": {"elementId": "box1", "gap": 5, "focus": 0},
        "endBinding": None,
    }
    errors, _ = validate(_write(tmp_path, _minimal_data(box, arrow)))
    assert errors == []


# ---------------------------------------------------------------------------
# Spatial checks
# ---------------------------------------------------------------------------

def test_off_canvas_x(tmp_path: Path):
    el = _rect("off1", x=-500, y=100)
    el2 = _rect("el2", x=300, y=100)
    errors, _ = validate(_write(tmp_path, _minimal_data(el, el2)))
    assert any("off-canvas" in e.lower() or "x=" in e for e in errors)


def test_off_canvas_y(tmp_path: Path):
    el = _rect("off1", x=100, y=-500)
    el2 = _rect("el2", x=300, y=300)
    errors, _ = validate(_write(tmp_path, _minimal_data(el, el2)))
    assert any("off-canvas" in e.lower() or "y=" in e for e in errors)


def test_coordinate_collision(tmp_path: Path):
    # Same x, y, width, height — definite copy-paste collision
    el1 = {"id": "el1", "type": "rectangle", "x": 100, "y": 100, "width": 150, "height": 80}
    el2 = {"id": "el2", "type": "rectangle", "x": 100, "y": 100, "width": 150, "height": 80}
    errors, _ = validate(_write(tmp_path, _minimal_data(el1, el2)))
    assert any("collision" in e.lower() or "identical" in e.lower() for e in errors)


def test_stacked_spread(tmp_path: Path):
    # 4 elements all within a tiny area
    elements = [_rect(f"el{i}", x=50 + i, y=50 + i) for i in range(4)]
    errors, _ = validate(_write(tmp_path, _minimal_data(*elements)))
    # Should catch either collision or spread error
    assert len(errors) > 0


def test_well_spread_elements_pass(tmp_path: Path):
    elements = [
        _rect("el1", x=80,  y=80),
        _rect("el2", x=400, y=80),
        _rect("el3", x=800, y=80),
        _rect("el4", x=80,  y=400),
    ]
    errors, _ = validate(_write(tmp_path, _minimal_data(*elements)))
    assert errors == []


# ---------------------------------------------------------------------------
# Style warnings (non-blocking)
# ---------------------------------------------------------------------------

def test_non_virgil_font_is_warning_not_error(tmp_path: Path):
    el = {
        "id": "txt1", "type": "text",
        "x": 100, "y": 100, "width": 200, "height": 20,
        "text": "hello", "fontFamily": 3, "fontSize": 16, "autoResize": True,
    }
    errors, warnings = validate(_write(tmp_path, _minimal_data(el)))
    assert errors == []
    assert any("fontFamily" in w for w in warnings)


def test_roughness_zero_is_warning_not_error(tmp_path: Path):
    el = {**_rect("el1"), "roughness": 0}
    el2 = _rect("el2", x=400, y=300)
    errors, warnings = validate(_write(tmp_path, _minimal_data(el, el2)))
    assert errors == []
    assert any("roughness" in w for w in warnings)


def test_virgil_font_no_warning(tmp_path: Path):
    el = {
        "id": "txt1", "type": "text",
        "x": 100, "y": 100, "width": 200, "height": 20,
        "text": "hello", "fontFamily": 1, "fontSize": 16, "autoResize": True,
    }
    errors, warnings = validate(_write(tmp_path, _minimal_data(el)))
    assert errors == []
    assert not any("fontFamily" in w for w in warnings)
