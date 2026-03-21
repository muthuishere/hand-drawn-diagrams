"""E2E tests for render_excalidraw.py — requires Playwright + Chromium.

Run all:        uv run pytest tests/
Skip slow:      uv run pytest tests/ -m "not slow"
Slow only:      uv run pytest tests/ -m slow
"""
from __future__ import annotations

import shutil

import pytest

from conftest import VALID_FILE
from render_excalidraw import render

pytestmark = pytest.mark.slow


def test_render_png_exists(tmp_path):
    output = tmp_path / "out.png"
    result = render(VALID_FILE, output_path=output)
    assert result == output
    assert output.exists()


def test_render_png_is_nonempty(tmp_path):
    output = tmp_path / "out.png"
    render(VALID_FILE, output_path=output)
    assert output.stat().st_size > 20_000  # real diagram PNG is well over 20KB


def test_render_writes_svg_alongside_png(tmp_path):
    output = tmp_path / "out.png"
    render(VALID_FILE, output_path=output)
    svg = output.with_suffix(".svg")
    assert svg.exists()
    assert svg.stat().st_size > 5_000


def test_render_svg_content_is_valid(tmp_path):
    output = tmp_path / "out.png"
    render(VALID_FILE, output_path=output)
    svg_content = output.with_suffix(".svg").read_text(encoding="utf-8")
    assert svg_content.strip().startswith("<svg") or "<?xml" in svg_content
    assert "</svg>" in svg_content


def test_render_svg_only_no_png(tmp_path):
    output = tmp_path / "out.png"
    result = render(VALID_FILE, output_path=output, svg_only=True)
    # Should return the SVG path, not PNG
    assert result.suffix == ".svg"
    assert result.exists()
    assert not output.exists()  # PNG must NOT be created


def test_render_svg_only_content_valid(tmp_path):
    output = tmp_path / "out.png"
    svg_path = render(VALID_FILE, output_path=output, svg_only=True)
    content = svg_path.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "</svg>" in content


def test_render_default_output_path(tmp_path):
    """When no output_path is given, file is placed next to the source."""
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)
    result = render(src)
    assert result.parent == tmp_path
    assert result.suffix == ".png"
    assert result.exists()


def test_render_scale_2(tmp_path):
    """Scale=2 should produce a larger PNG than scale=1."""
    out1 = tmp_path / "scale1.png"
    out2 = tmp_path / "scale2.png"
    render(VALID_FILE, output_path=out1, scale=1)
    render(VALID_FILE, output_path=out2, scale=2)
    assert out2.stat().st_size > out1.stat().st_size
