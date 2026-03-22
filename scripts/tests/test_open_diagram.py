"""Tests for open_diagram.py — fast, no browser launch, no Playwright required."""
from __future__ import annotations

import shutil

import pytest

from conftest import VALID_FILE
from open_diagram import _open_animate, _open_edit, _save_excalidraw, _write_redirect
from hosted_scene_urls import build_edit_url, build_animate_url


# ---------------------------------------------------------------------------
# Redirect HTML helpers
# ---------------------------------------------------------------------------

def test_redirect_html_is_written(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    launcher = _write_redirect(src, url, "edit")

    assert launcher.exists()
    assert launcher.name == "open-edit.html"


def test_redirect_html_contains_target_url(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    launcher = _write_redirect(src, url, "edit")
    content = launcher.read_text(encoding="utf-8")

    assert "window.location.replace" in content
    assert "edit.html#" in content


def test_redirect_html_has_no_buttons(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    launcher = _write_redirect(src, url, "edit")
    content = launcher.read_text(encoding="utf-8")

    assert "<button" not in content
    assert "btn-" not in content


def test_redirect_html_is_valid_html(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    launcher = _write_redirect(src, url, "edit")
    content = launcher.read_text(encoding="utf-8")

    assert content.startswith("<!DOCTYPE html>")
    assert "</html>" in content


def test_edit_and_animate_get_separate_files(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    edit_launcher = _write_redirect(src, build_edit_url(src), "edit")
    anim_launcher = _write_redirect(src, build_animate_url(src), "animate")

    assert edit_launcher.name == "open-edit.html"
    assert anim_launcher.name == "open-animate.html"
    assert edit_launcher != anim_launcher


def test_animate_redirect_targets_animate_url(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_animate_url(src)
    launcher = _write_redirect(src, url, "animate")
    content = launcher.read_text(encoding="utf-8")

    assert "animate.html#" in content


def test_url_is_html_escaped_in_redirect(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    launcher = _write_redirect(src, url, "edit")
    content = launcher.read_text(encoding="utf-8")

    # Raw unescaped & must not appear inside the script string
    import re
    # extract the URL inside window.location.replace("...")
    match = re.search(r'window\.location\.replace\("([^"]+)"\)', content)
    assert match, "replace() call not found"
    embedded = match.group(1)
    assert "&" not in embedded  # only &amp; after escaping, but base64 rarely has &


def test_overwrite_is_idempotent(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    url = build_edit_url(src)
    l1 = _write_redirect(src, url, "edit")
    l2 = _write_redirect(src, url, "edit")

    assert l1.read_text() == l2.read_text()


# ---------------------------------------------------------------------------
# save-excalidraw mode
# ---------------------------------------------------------------------------

def test_save_excalidraw_copies_file(tmp_path):
    src_dir = tmp_path / "source"
    src_dir.mkdir()
    src = src_dir / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    dest = tmp_path / "project"
    _save_excalidraw(src, dest)

    assert (dest / VALID_FILE.name).exists()


def test_save_excalidraw_creates_dest_if_missing(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    dest = tmp_path / "new" / "nested" / "dir"
    _save_excalidraw(src, dest)

    assert (dest / VALID_FILE.name).exists()


def test_save_excalidraw_copies_animationinfo_when_present(tmp_path):
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)
    anim = tmp_path / src.with_suffix(".animationinfo.json").name
    anim.write_text('{"startMs":0,"defaultDuration":400,"elements":[]}', encoding="utf-8")

    dest = tmp_path / "project"
    _save_excalidraw(src, dest)

    assert (dest / anim.name).exists()


# ---------------------------------------------------------------------------
# --no-open flag (smoke: ensure no browser is launched in CI)
# ---------------------------------------------------------------------------

def test_open_edit_no_open_writes_launcher(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr("webbrowser.open", lambda u: opened.append(u))
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    _open_edit(src, no_open=True)

    assert not opened
    assert (tmp_path / "open-edit.html").exists()


def test_open_animate_no_open_writes_launcher(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr("webbrowser.open", lambda u: opened.append(u))
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    _open_animate(src, no_open=True)

    assert not opened
    assert (tmp_path / "open-animate.html").exists()


def test_open_edit_opens_browser_by_default(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr("webbrowser.open", lambda u: opened.append(u))
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)

    _open_edit(src, no_open=False)

    assert len(opened) == 1
    assert "open-edit.html" in opened[0]
