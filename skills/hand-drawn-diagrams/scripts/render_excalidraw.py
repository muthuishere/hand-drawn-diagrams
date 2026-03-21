"""Render Excalidraw JSON to PNG using Playwright + headless Chromium.

Usage:
    cd {skill-root}/scripts
    uv run python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2] [--width 1920]

First-time setup:
    cd <installed-skill>/scripts && uv sync && uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from local_excalidraw_server import LocalExcalidrawServer


RENDER_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #ffffff; overflow: hidden; }
    #root { display: inline-block; }
    #root svg { display: block; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="module">
    window.__moduleReady = false;
    window.__moduleError = null;
    window.__renderComplete = false;
    window.__renderError = null;

    try {
      const mod = await import("/@excalidraw/excalidraw?bundle");
      const { exportToSvg } = mod;

      window.renderDiagram = async function(jsonData) {
        window.__renderComplete = false;
        window.__renderError = null;

        try {
          const data = typeof jsonData === "string" ? JSON.parse(jsonData) : jsonData;
          const elements = data.elements || [];
          const appState = data.appState || {};
          const files = data.files || {};

          appState.viewBackgroundColor = appState.viewBackgroundColor || "#ffffff";
          appState.exportWithDarkMode = false;

          const svg = await exportToSvg({
            elements,
            appState: {
              ...appState,
              exportBackground: true,
            },
            files,
          });

          const root = document.getElementById("root");
          root.innerHTML = "";
          root.appendChild(svg);

          // Serialise the SVG to a string so Python can grab it without a screenshot.
          const svgString = new XMLSerializer().serializeToString(svg);

          window.__renderComplete = true;
          return {
            success: true,
            width: svg.getAttribute("width"),
            height: svg.getAttribute("height"),
            svgString,
          };
        } catch (err) {
          window.__renderError = err?.message || String(err);
          window.__renderComplete = true;
          return { success: false, error: window.__renderError };
        }
      };

      window.__moduleReady = true;
    } catch (err) {
      window.__moduleError = err?.message || String(err);
    }
  </script>
</body>
</html>
"""


def setup_marker(scripts_dir: Path) -> Path:
    return scripts_dir / ".setup_complete"


def ensure_render_runtime_ready(scripts_dir: Path) -> None:
    marker = setup_marker(scripts_dir)
    if marker.is_file():
        return

    if not shutil.which("uv"):
        print("ERROR: uv is required for first-time render setup.", file=sys.stderr)
        print("Install uv and retry the render command.", file=sys.stderr)
        sys.exit(1)

    print("First-time render setup: installing Chromium for Playwright...", file=sys.stderr)

    completed = subprocess.run(["uv", "sync"], cwd=scripts_dir, check=False)
    if completed.returncode == 0:
        completed = subprocess.run(
            ["uv", "run", "playwright", "install", "chromium"],
            cwd=scripts_dir,
            check=False,
        )

    if completed.returncode != 0:
        print("ERROR: First-time render setup failed.", file=sys.stderr)
        print(
            f"Run manually: cd {scripts_dir} && uv sync && uv run playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(completed.returncode or 1)

    marker.touch()
    print("Render setup complete.", file=sys.stderr)


def validate_excalidraw(data: dict) -> list[str]:
    """Validate Excalidraw JSON structure. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if data.get("type") != "excalidraw":
        errors.append(f"Expected type 'excalidraw', got '{data.get('type')}'")

    if "elements" not in data:
        errors.append("Missing 'elements' array")
    elif not isinstance(data["elements"], list):
        errors.append("'elements' must be an array")
    elif len(data["elements"]) == 0:
        errors.append("'elements' array is empty — nothing to render")

    return errors


def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute bounding box (min_x, min_y, max_x, max_y) across all elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)

        # For arrows/lines, points array defines the shape relative to x,y
        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def _run_browser(
    excalidraw_path: Path,
    data: dict,
    vp_width: int,
    vp_height: int,
    scale: int,
    svg_output: Path | None,
    png_output: Path | None,
) -> None:
    """Launch Playwright, call renderDiagram, write SVG and/or PNG."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        print("Run: uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(1)

    server = LocalExcalidrawServer(
        pages={"/render.html": (RENDER_HTML, "text/html; charset=utf-8")},
    )
    server.start()

    with sync_playwright() as p:
        browser = None
        try:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                    print("ERROR: Chromium not installed for Playwright.", file=sys.stderr)
                    print("Run: uv run playwright install chromium", file=sys.stderr)
                    sys.exit(1)
                raise

            page = browser.new_page(
                viewport={"width": vp_width, "height": vp_height},
                device_scale_factor=scale,
            )
            page.set_default_timeout(30000)

            console_messages: list[str] = []
            request_failures: list[str] = []
            page_errors: list[str] = []

            page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))
            page.on("requestfailed", lambda req: request_failures.append(
                f"{req.url} :: {req.failure.error_text if req.failure else 'failed'}"
            ))
            page.on("pageerror", lambda err: page_errors.append(str(err)))

            page.goto(server.url_for("/render.html"), wait_until="load")
            page.wait_for_function("window.__moduleReady === true || window.__moduleError !== null")

            module_state = page.evaluate("() => ({ready: window.__moduleReady, error: window.__moduleError})")
            if module_state.get("error"):
                raise RuntimeError(f"Module load failed: {module_state['error']}")

            json_str = json.dumps(data)
            result = page.evaluate(f"window.renderDiagram({json_str})")
            if not result or not result.get("success"):
                error_msg = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
                raise RuntimeError(f"Render failed: {error_msg}")

            page.wait_for_function("window.__renderComplete === true")

            # Write SVG using the string already serialised in JS (no extra round-trip)
            svg_string = result.get("svgString")
            if svg_output and svg_string:
                svg_output.write_text(svg_string, encoding="utf-8")

            # Write PNG via element screenshot only when a PNG is actually requested
            if png_output:
                svg_el = page.query_selector("#root svg")
                if svg_el is None:
                    raise RuntimeError("No SVG element found after render")
                svg_el.screenshot(path=str(png_output))

        except Exception as exc:
            debug_parts = [f"ERROR: {exc}"]
            if page_errors:
                debug_parts.append("Page errors:")
                debug_parts.extend(f"  - {err}" for err in page_errors[-5:])
            if request_failures:
                debug_parts.append("Request failures:")
                debug_parts.extend(f"  - {err}" for err in request_failures[-10:])
            if console_messages:
                debug_parts.append("Console messages:")
                debug_parts.extend(f"  - {msg}" for msg in console_messages[-10:])
            print("\n".join(debug_parts), file=sys.stderr)
            sys.exit(1)
        finally:
            if browser is not None:
                browser.close()
            server.close()


def render(
    excalidraw_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
    svg_only: bool = False,
) -> Path:
    """Render an .excalidraw file to PNG (and optionally SVG). Returns output path."""
    scripts_dir = Path(__file__).parent
    ensure_render_runtime_ready(scripts_dir)

    # Read and validate
    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {excalidraw_path}: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_excalidraw(data)
    if errors:
        print("ERROR: Invalid Excalidraw file:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Compute viewport size from element bounding box
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    min_x, min_y, max_x, max_y = compute_bounding_box(elements)
    padding = 80
    diagram_w = max_x - min_x + padding * 2
    diagram_h = max_y - min_y + padding * 2

    vp_width = min(int(diagram_w), max_width)
    vp_height = max(int(diagram_h), 600)

    # Resolve output paths
    svg_output: Path | None = None
    png_output: Path | None = None

    if svg_only:
        svg_output = (output_path or excalidraw_path).with_suffix(".svg")
    else:
        png_output = output_path or excalidraw_path.with_suffix(".png")
        svg_output = png_output.with_suffix(".svg")  # write SVG alongside PNG for free

    _run_browser(excalidraw_path, data, vp_width, vp_height, scale, svg_output, png_output)

    final_path = svg_output if svg_only else png_output
    return final_path  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG")
    parser.add_argument("input", type=Path, help="Path to .excalidraw JSON file")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output path (default: same name with .png or .svg)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max viewport width (default: 1920)")
    parser.add_argument("--svg-only", action="store_true", help="Export SVG only — faster, skips PNG screenshot")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    out_path = render(args.input, args.output, args.scale, args.width, args.svg_only)
    print(str(out_path))


if __name__ == "__main__":
    main()
