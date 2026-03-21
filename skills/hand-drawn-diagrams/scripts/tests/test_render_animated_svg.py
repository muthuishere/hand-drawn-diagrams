"""E2E tests for render_animated_svg.py — requires Playwright + Chromium.

Run all:    uv run pytest tests/
Skip slow:  uv run pytest tests/ -m "not slow"
Slow only:  uv run pytest tests/ -m slow
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from conftest import VALID_FILE
from render_animated_svg import (
    apply_animation_info,
    discover_animation_info,
    load_animation_info,
    render_animated_svg,
)

pytestmark = pytest.mark.slow


# ---------------------------------------------------------------------------
# Helper — build a minimal animationinfo.json for the test diagram
# ---------------------------------------------------------------------------

def _write_animationinfo(excalidraw_path: Path) -> Path:
    """Write a companion .animationinfo.json next to excalidraw_path."""
    data = json.loads(excalidraw_path.read_text(encoding="utf-8"))
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    # Spread elements across 10 groups of sequential order values
    group_size = max(1, len(elements) // 10)
    anim_elements = [
        {"id": e["id"], "order": (i // group_size) + 1, "duration": 300}
        for i, e in enumerate(elements)
    ]
    info = {"startMs": 300, "defaultDuration": 300, "elements": anim_elements}
    info_path = excalidraw_path.with_suffix(".animationinfo.json")
    info_path.write_text(json.dumps(info), encoding="utf-8")
    return info_path


# ---------------------------------------------------------------------------
# Unit tests for helper functions (no Playwright)
# ---------------------------------------------------------------------------

class TestDiscoverAnimationInfo:
    def test_finds_companion_file(self, tmp_path):
        src = tmp_path / "diagram.excalidraw"
        src.write_text("{}", encoding="utf-8")
        companion = tmp_path / "diagram.animationinfo.json"
        companion.write_text("{}", encoding="utf-8")
        assert discover_animation_info(src) == companion

    def test_returns_none_when_missing(self, tmp_path):
        src = tmp_path / "diagram.excalidraw"
        src.write_text("{}", encoding="utf-8")
        assert discover_animation_info(src) is None


class TestLoadAnimationInfo:
    def test_loads_valid_json(self, tmp_path):
        f = tmp_path / "spec.json"
        f.write_text('{"startMs": 500, "elements": []}', encoding="utf-8")
        info = load_animation_info(f)
        assert info["startMs"] == 500

    def test_returns_empty_dict_for_none(self):
        assert load_animation_info(None) == {}

    def test_returns_empty_dict_for_missing_file(self, tmp_path):
        assert load_animation_info(tmp_path / "ghost.json") == {}


class TestApplyAnimationInfo:
    def test_injects_order_and_duration(self):
        elements = [{"id": "box1", "type": "rectangle"}]
        info = {"elements": [{"id": "box1", "order": 3, "duration": 600}]}
        result = apply_animation_info(elements, info, default_duration=500)
        assert len(result) == 1
        assert "animateOrder:3" in result[0]["id"]
        assert "animateDuration:600" in result[0]["id"]

    def test_injects_default_duration_for_unspecified(self):
        elements = [{"id": "box2", "type": "text"}]
        result = apply_animation_info(elements, {}, default_duration=400)
        assert "animateDuration:400" in result[0]["id"]

    def test_does_not_mutate_original_elements(self):
        original = [{"id": "box1", "type": "rectangle"}]
        info = {"elements": [{"id": "box1", "order": 1, "duration": 500}]}
        apply_animation_info(original, info, default_duration=500)
        assert original[0]["id"] == "box1"  # unchanged

    def test_element_without_override_still_gets_duration_suffix(self):
        elements = [{"id": "arrow1", "type": "arrow"}]
        result = apply_animation_info(elements, {}, default_duration=350)
        assert result[0]["id"] != "arrow1"
        assert "animateDuration:350" in result[0]["id"]


# ---------------------------------------------------------------------------
# E2E render tests (Playwright)
# ---------------------------------------------------------------------------

@pytest.fixture
def diagram_with_info(tmp_path):
    """Copy the test excalidraw + write companion animationinfo.json to tmp_path."""
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)
    _write_animationinfo(src)
    return src


def test_render_produces_output_file(diagram_with_info, tmp_path):
    output = tmp_path / "out.animated.svg"
    result = render_animated_svg(diagram_with_info, output_path=output)
    assert result == output
    assert output.exists()


def test_render_output_is_nonempty(diagram_with_info, tmp_path):
    output = tmp_path / "out.animated.svg"
    render_animated_svg(diagram_with_info, output_path=output)
    assert output.stat().st_size > 10_000


def test_render_output_is_valid_svg(diagram_with_info, tmp_path):
    output = tmp_path / "out.animated.svg"
    render_animated_svg(diagram_with_info, output_path=output)
    content = output.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "</svg>" in content


def test_render_output_contains_animate_elements(diagram_with_info, tmp_path):
    output = tmp_path / "out.animated.svg"
    render_animated_svg(diagram_with_info, output_path=output)
    content = output.read_text(encoding="utf-8")
    assert "<animate" in content


def test_render_auto_discovers_animationinfo(diagram_with_info, tmp_path):
    """No explicit animation_path arg — companion file should be found automatically."""
    output = tmp_path / "auto.animated.svg"
    render_animated_svg(diagram_with_info, animation_path=None, output_path=output)
    assert output.exists()
    assert output.stat().st_size > 10_000


def test_render_explicit_animation_path(diagram_with_info, tmp_path):
    companion = diagram_with_info.with_suffix(".animationinfo.json")
    output = tmp_path / "explicit.animated.svg"
    render_animated_svg(diagram_with_info, animation_path=companion, output_path=output)
    assert output.exists()


def test_render_default_output_path(diagram_with_info):
    """When no output_path is given, file lands next to the source."""
    expected = diagram_with_info.with_suffix(".animated.svg")
    try:
        result = render_animated_svg(diagram_with_info)
        assert result == expected
        assert expected.exists()
    finally:
        if expected.exists():
            expected.unlink()


def test_render_returns_path_object(diagram_with_info, tmp_path):
    output = tmp_path / "out.animated.svg"
    result = render_animated_svg(diagram_with_info, output_path=output)
    assert isinstance(result, Path)
