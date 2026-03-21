from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path


PAGES_BASE_URL = "https://muthuishere.github.io/hand-drawn-diagrams"
EDIT_URL = f"{PAGES_BASE_URL}/edit.html"
ANIMATE_URL = f"{PAGES_BASE_URL}/animate.html"


def encode_bundle(
    excalidraw_path: Path,
    animationinfo_path: Path | None = None,
) -> str:
    """Gzip+base64 encode a bundle of excalidraw + optional animationInfo.

    Bundle format:
        { "excalidraw": {...}, "animationInfo": {...} }

    The receive side detects the new format by checking for the "excalidraw" key.
    Old URLs (raw excalidraw JSON) remain readable — the receive side falls back
    to treating the whole payload as excalidraw data.
    """
    excalidraw_data = json.loads(excalidraw_path.read_text(encoding="utf-8"))
    bundle: dict = {"excalidraw": excalidraw_data}

    if animationinfo_path and animationinfo_path.exists():
        bundle["animationInfo"] = json.loads(
            animationinfo_path.read_text(encoding="utf-8")
        )

    raw = json.dumps(bundle, separators=(",", ":"))
    compressed = gzip.compress(raw.encode("utf-8"), compresslevel=9)
    return base64.b64encode(compressed).decode("ascii")


def discover_animationinfo(excalidraw_path: Path) -> Path | None:
    """Return the companion .animationinfo.json if it exists alongside the diagram."""
    candidate = excalidraw_path.with_suffix(".animationinfo.json")
    return candidate if candidate.exists() else None


def build_edit_url(
    path: Path,
    animationinfo_path: Path | None = None,
) -> str:
    anim = animationinfo_path if animationinfo_path is not None else discover_animationinfo(path)
    return f"{EDIT_URL}#{encode_bundle(path, anim)}"


def build_animate_url(
    path: Path,
    animationinfo_path: Path | None = None,
) -> str:
    anim = animationinfo_path if animationinfo_path is not None else discover_animationinfo(path)
    return f"{ANIMATE_URL}#{encode_bundle(path, anim)}"


# ---------------------------------------------------------------------------
# Legacy helper — kept for backward compat with animate_excalidraw.py
# ---------------------------------------------------------------------------

def encode_diagram(path: Path) -> str:
    """Encode just the excalidraw file (no animationInfo). Legacy format."""
    raw = path.read_text(encoding="utf-8")
    compressed = gzip.compress(raw.encode("utf-8"), compresslevel=9)
    return base64.b64encode(compressed).decode("ascii")
