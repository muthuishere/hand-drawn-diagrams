"""Tests for hosted_scene_urls.py — fast, no Playwright required."""
from __future__ import annotations

import base64
import gzip
import json

from conftest import VALID_FILE
from hosted_scene_urls import (
    ANIMATE_URL,
    EDIT_URL,
    build_animate_url,
    build_edit_url,
    encode_diagram,
)


def test_encode_produces_valid_base64():
    encoded = encode_diagram(VALID_FILE)
    # Must not raise
    decoded_bytes = base64.b64decode(encoded)
    assert len(decoded_bytes) > 0


def test_encode_round_trips_to_original_json():
    encoded = encode_diagram(VALID_FILE)
    compressed = base64.b64decode(encoded)
    raw = gzip.decompress(compressed).decode("utf-8")
    data = json.loads(raw)
    assert data["type"] == "excalidraw"
    assert len(data["elements"]) == 115


def test_encode_is_deterministic():
    a = encode_diagram(VALID_FILE)
    b = encode_diagram(VALID_FILE)
    assert a == b


def test_encode_is_smaller_than_raw():
    encoded = encode_diagram(VALID_FILE)
    raw_size = len(VALID_FILE.read_bytes())
    # gzip + base64 overhead: base64 is ~4/3× but gzip gives ~4-10× compression
    # For a 90KB JSON file the encoded string should be well under raw size
    assert len(encoded) < raw_size


def test_build_edit_url_uses_edit_base():
    url = build_edit_url(VALID_FILE)
    base, _ = url.split("#", 1)
    assert base == EDIT_URL


def test_build_animate_url_uses_animate_base():
    url = build_animate_url(VALID_FILE)
    base, _ = url.split("#", 1)
    assert base == ANIMATE_URL


def test_urls_share_same_hash():
    """Both URLs encode the same diagram — only the base differs."""
    edit_hash = build_edit_url(VALID_FILE).split("#", 1)[1]
    anim_hash = build_animate_url(VALID_FILE).split("#", 1)[1]
    assert edit_hash == anim_hash


def test_edit_and_animate_base_urls_differ():
    edit_base = build_edit_url(VALID_FILE).split("#")[0]
    anim_base = build_animate_url(VALID_FILE).split("#")[0]
    assert edit_base != anim_base


def test_url_hash_is_nonempty():
    url = build_edit_url(VALID_FILE)
    assert "#" in url
    hash_part = url.split("#", 1)[1]
    assert len(hash_part) > 100  # substantial encoded content


def test_bundle_without_animationinfo_has_no_animationinfo_key():
    url = build_edit_url(VALID_FILE)  # no companion .animationinfo.json for this file
    hash_part = url.split("#", 1)[1]
    bundle = json.loads(gzip.decompress(base64.b64decode(hash_part)).decode("utf-8"))
    assert "animationInfo" not in bundle


def test_bundle_with_animationinfo_includes_it(tmp_path):
    import shutil
    src = tmp_path / VALID_FILE.name
    shutil.copy(VALID_FILE, src)
    info = tmp_path / src.with_suffix(".animationinfo.json").name
    info.write_text('{"startMs":500,"defaultDuration":400,"elements":[]}', encoding="utf-8")
    url = build_edit_url(src)
    hash_part = url.split("#", 1)[1]
    bundle = json.loads(gzip.decompress(base64.b64decode(hash_part)).decode("utf-8"))
    assert "animationInfo" in bundle
    assert bundle["animationInfo"]["startMs"] == 500


def test_url_hash_decodes_to_valid_bundle():
    """Hash now contains {excalidraw: {...}, animationInfo?: {...}} bundle."""
    url = build_edit_url(VALID_FILE)
    hash_part = url.split("#", 1)[1]
    raw = gzip.decompress(base64.b64decode(hash_part)).decode("utf-8")
    bundle = json.loads(raw)
    # New bundle format
    assert "excalidraw" in bundle
    excalidraw = bundle["excalidraw"]
    assert excalidraw.get("type") == "excalidraw"
    assert isinstance(excalidraw.get("elements"), list)
    assert len(excalidraw["elements"]) > 0
