"""Render an Excalidraw file to a self-contained animated SVG using Playwright.

Reads a `.excalidraw` file and an optional `.animationinfo.json` companion,
injects per-element animateOrder / animateDuration into element IDs, runs
excalidraw-animate in headless Chromium, and writes a `.animated.svg` that
plays in any browser.

Usage:
    cd {skill-root}/scripts
    uv run python render_animated_svg.py diagram.excalidraw

    # with explicit animation spec
    uv run python render_animated_svg.py diagram.excalidraw \\
        --animation diagram.animationinfo.json

    # custom output path
    uv run python render_animated_svg.py diagram.excalidraw \\
        --output diagram.animated.svg

    # override timing without editing the JSON
    uv run python render_animated_svg.py diagram.excalidraw \\
        --start-ms 1000 --default-duration 400

    # open the SVG in the default browser after writing
    uv run python render_animated_svg.py diagram.excalidraw --open

First-time setup (shared with render_excalidraw.py):
    cd {skill-root}/scripts && uv sync && uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from local_excalidraw_server import LocalExcalidrawServer


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def setup_marker(scripts_dir: Path) -> Path:
    return scripts_dir / ".setup_complete"


def ensure_render_runtime_ready(scripts_dir: Path) -> None:
    marker = setup_marker(scripts_dir)
    if marker.is_file():
        return

    if not shutil.which("uv"):
        print("ERROR: uv is required for first-time setup.", file=sys.stderr)
        sys.exit(1)

    print("First-time setup: installing Chromium for Playwright...", file=sys.stderr)
    completed = subprocess.run(["uv", "sync"], cwd=scripts_dir, check=False)
    if completed.returncode == 0:
        completed = subprocess.run(
            ["uv", "run", "playwright", "install", "chromium"],
            cwd=scripts_dir,
            check=False,
        )

    if completed.returncode != 0:
        print("ERROR: First-time setup failed.", file=sys.stderr)
        print(
            f"Run manually: cd {scripts_dir} && uv sync && uv run playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(completed.returncode or 1)

    marker.touch()
    print("Render setup complete.", file=sys.stderr)


# ---------------------------------------------------------------------------
# animationinfo helpers
# ---------------------------------------------------------------------------

def discover_animation_info(excalidraw_path: Path) -> Path | None:
    """Return the companion .animationinfo.json path if it exists."""
    candidate = excalidraw_path.with_suffix(".animationinfo.json")
    return candidate if candidate.exists() else None


def load_animation_info(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def apply_animation_info(
    elements: list[dict],
    anim_info: dict,
    default_duration: int,
) -> list[dict]:
    """
    Return a shallow copy of elements with animateOrder:N and animateDuration:N
    suffixes injected into element IDs from anim_info.

    The original elements list is never mutated.
    The excalidraw-animate library reads these suffixes from element IDs
    to determine animation order and per-element duration.
    """
    overrides: dict[str, dict] = {}
    for entry in anim_info.get("elements", []):
        eid = entry.get("id")
        if eid:
            overrides[eid] = entry

    result: list[dict] = []
    for el in elements:
        eid = el.get("id", "")
        ov = overrides.get(eid)
        if ov:
            suffix_parts: list[str] = []
            if "order" in ov:
                suffix_parts.append(f"animateOrder:{ov['order']}")
            dur = ov.get("duration", default_duration)
            suffix_parts.append(f"animateDuration:{dur}")
            new_id = eid + "-" + "-".join(suffix_parts) if suffix_parts else eid
            result.append({**el, "id": new_id})
        else:
            # No explicit override: inject default duration for consistency
            new_id = f"{eid}-animateDuration:{default_duration}"
            result.append({**el, "id": new_id})
    return result


# ---------------------------------------------------------------------------
# Playwright runner
# ---------------------------------------------------------------------------

def _load_animatecreator_html() -> str:
    html_path = Path(__file__).parent / "animatecreator.html"
    if not html_path.exists():
        raise FileNotFoundError(
            f"animatecreator.html not found at {html_path}.\n"
            "It should be in the same directory as this script."
        )
    return html_path.read_text(encoding="utf-8")


def _run_browser(
    data: dict,
    start_ms: int,
    output_path: Path,
) -> float:
    """Launch Playwright, call renderAnimation, write animated SVG. Returns finishedMs."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        print("Run: uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(1)

    html_content = _load_animatecreator_html()

    server = LocalExcalidrawServer(
        pages={"/animatecreator.html": (html_content, "text/html; charset=utf-8")},
    )
    server.start()

    finished_ms: float = 0.0

    with sync_playwright() as p:
        browser = None
        try:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                    print("ERROR: Chromium not installed.", file=sys.stderr)
                    print("Run: uv run playwright install chromium", file=sys.stderr)
                    sys.exit(1)
                raise

            page = browser.new_page(viewport={"width": 1600, "height": 900})
            page.set_default_timeout(60000)

            page_errors: list[str] = []
            request_failures: list[str] = []
            page.on("pageerror", lambda e: page_errors.append(str(e)))
            page.on("requestfailed", lambda r: request_failures.append(
                f"{r.url} :: {r.failure if isinstance(r.failure, str) else (r.failure.error_text if r.failure else 'failed')}"
            ))

            page.goto(server.url_for("/animatecreator.html"), wait_until="load")

            # Wait for both excalidraw + excalidraw-animate to load from ESM cache
            page.wait_for_function(
                "window.__ready === true || window.__moduleError !== null",
                timeout=60000,
            )

            module_state = page.evaluate(
                "() => ({ ready: window.__ready, error: window.__moduleError })"
            )
            if module_state.get("error"):
                raise RuntimeError(f"Module load failed: {module_state['error']}")

            # Pass JSON string and startMs; Playwright JSON-serialises the call args
            json_str = json.dumps(data)
            result = page.evaluate(
                "([jsonStr, startMs]) => window.renderAnimation(jsonStr, startMs)",
                [json_str, start_ms],
            )

            if not result or result.get("error"):
                err = (result.get("error", "renderAnimation returned null")
                       if result else "null result")
                raise RuntimeError(f"Animation render failed: {err}")

            svg_string: str = result["svgString"]
            finished_ms = float(result.get("finishedMs", 0))

            output_path.write_text(svg_string, encoding="utf-8")

        except Exception as exc:
            parts = [f"ERROR: {exc}"]
            if page_errors:
                parts += ["Page errors:"] + [f"  - {e}" for e in page_errors[-5:]]
            if request_failures:
                parts += ["Request failures:"] + [f"  - {r}" for r in request_failures[-10:]]
            print("\n".join(parts), file=sys.stderr)
            sys.exit(1)
        finally:
            if browser:
                browser.close()
            server.close()

    return finished_ms


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render_animated_svg(
    excalidraw_path: Path,
    animation_path: Path | None = None,
    output_path: Path | None = None,
    start_ms: int = 500,
    default_duration: int = 500,
    open_browser: bool = False,
) -> Path:
    """
    Produce a self-contained animated SVG from an Excalidraw file.

    Parameters
    ----------
    excalidraw_path   Path to the .excalidraw source file.
    animation_path    Path to .animationinfo.json. Auto-discovered if None.
    output_path       Output path. Defaults to <excalidraw_path>.animated.svg.
    start_ms          Initial pause before animation (ms).
    default_duration  Duration for elements without an explicit override (ms).
    open_browser      Open the SVG in the default browser after writing.

    Returns
    -------
    Path to the written .animated.svg file.
    """
    scripts_dir = Path(__file__).parent
    ensure_render_runtime_ready(scripts_dir)

    # Read + validate source
    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in {excalidraw_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    if data.get("type") != "excalidraw":
        print("ERROR: File is not a valid Excalidraw file.", file=sys.stderr)
        sys.exit(1)

    elements = [e for e in data.get("elements", []) if not e.get("isDeleted")]
    if not elements:
        print("ERROR: No elements — nothing to animate.", file=sys.stderr)
        sys.exit(1)

    # Resolve animation spec
    if animation_path is None:
        animation_path = discover_animation_info(excalidraw_path)

    anim_info = load_animation_info(animation_path)
    effective_start_ms = anim_info.get("startMs", start_ms)
    effective_default_dur = anim_info.get("defaultDuration", default_duration)

    if animation_path and animation_path.exists():
        print(f"Animation spec: {animation_path.name}", file=sys.stderr)
        spec_count = len(anim_info.get("elements", []))
        print(f"  {spec_count} element overrides, "
              f"startMs={effective_start_ms}, "
              f"defaultDuration={effective_default_dur}ms",
              file=sys.stderr)
    else:
        print(
            "No .animationinfo.json found — animating in natural element order.",
            file=sys.stderr,
        )

    # Inject animation IDs into element copies
    patched_elements = apply_animation_info(elements, anim_info, effective_default_dur)
    patched_data = {**data, "elements": patched_elements}

    # Output path
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".animated.svg")

    print(f"Rendering → {output_path.name} ...", file=sys.stderr)
    finished_ms = _run_browser(patched_data, effective_start_ms, output_path)

    secs = finished_ms / 1000
    size_kb = output_path.stat().st_size / 1024
    print(f"Done  duration={secs:.1f}s  size={size_kb:.0f}KB", file=sys.stderr)
    print(str(output_path))

    if open_browser:
        webbrowser.open(output_path.as_uri())

    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render an Excalidraw file to a self-contained animated SVG."
    )
    parser.add_argument("input", type=Path, help="Path to .excalidraw file")
    parser.add_argument(
        "--animation", "-a", type=Path, default=None,
        help="Path to .animationinfo.json (default: auto-discover <input>.animationinfo.json)",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Output path (default: <input>.animated.svg)",
    )
    parser.add_argument(
        "--start-ms", type=int, default=500,
        help="Initial pause before animation starts (ms, default: 500)",
    )
    parser.add_argument(
        "--default-duration", type=int, default=500,
        help="Duration for elements without an explicit override (ms, default: 500)",
    )
    parser.add_argument(
        "--open", action="store_true",
        help="Open the animated SVG in the default browser after writing",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    render_animated_svg(
        excalidraw_path=args.input,
        animation_path=args.animation,
        output_path=args.output,
        start_ms=args.start_ms,
        default_duration=args.default_duration,
        open_browser=args.open,
    )


if __name__ == "__main__":
    main()
