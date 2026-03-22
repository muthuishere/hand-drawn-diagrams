#!/usr/bin/env python3

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


SKILL_NAME = "hand-drawn-diagrams"


@dataclass(frozen=True)
class InstallTarget:
    key: str
    label: str
    cli_names: tuple[str, ...]
    relative_dir: str
    required: bool = False

    def target(self, home_dir: Path) -> Path:
        return home_dir / self.relative_dir / SKILL_NAME

    def detected(self) -> bool:
        return any(shutil.which(name) for name in self.cli_names)


TARGETS = (
    InstallTarget("agents", "Agent Skills", ("codex",), ".agents/skills", required=False),
    InstallTarget("claude", "Claude Code", ("claude",), ".claude/skills", required=False),
)


def repo_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def skill_dir() -> Path:
    return repo_dir()

def setup_marker(scripts_dir: Path) -> Path:
    return scripts_dir / ".setup_complete"


def render_venv_dir(scripts_dir: Path) -> Path:
    return scripts_dir / ".venv"


def home_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("USERPROFILE", str(Path.home())))
    return Path(os.environ.get("HOME", str(Path.home())))


def find_python_command() -> tuple[str | None, tuple[int, int, int] | None]:
    candidates = ["python3", "python"] if os.name != "nt" else ["python", "py -3", "py"]
    for candidate in candidates:
        try:
            completed = subprocess.run(
                f'{candidate} -c "import sys; print(\'.\'.join(map(str, sys.version_info[:3])))"',
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError:
            continue
        version_text = completed.stdout.strip()
        try:
            version = tuple(int(part) for part in version_text.split("."))
        except ValueError:
            continue
        return candidate, version  # type: ignore[return-value]
    return None, None


def uv_status() -> tuple[bool, str]:
    uv_cmd = shutil.which("uv")
    if not uv_cmd:
        return False, "missing"
    completed = subprocess.run([uv_cmd, "--version"], capture_output=True, text=True, check=False)
    version = completed.stdout.strip() or completed.stderr.strip() or "available"
    return True, f"available ({version})"


def chrome_devtools_mcp_status() -> tuple[bool, str]:
    """Check if chrome-devtools-mcp is installed (enables fast browser rendering — no Playwright needed)."""
    # Check npm global packages
    npm_cmd = shutil.which("npm")
    if npm_cmd:
        result = subprocess.run(
            [npm_cmd, "list", "-g", "--depth=0", "chrome-devtools-mcp"],
            capture_output=True, text=True, check=False,
        )
        if "chrome-devtools-mcp" in result.stdout:
            # Extract version
            for line in result.stdout.splitlines():
                if "chrome-devtools-mcp" in line:
                    version = line.strip().split("@")[-1] if "@" in line else "installed"
                    return True, f"installed ({version})"

    # Check npx can resolve it (works if installed locally or globally via npx cache)
    npx_cmd = shutil.which("npx")
    if npx_cmd:
        result = subprocess.run(
            [npx_cmd, "--yes=false", "chrome-devtools-mcp", "--version"],
            capture_output=True, text=True, check=False, timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.strip() or "available"
            return True, f"available via npx ({version})"

    return False, "not found — install with: npm install -g chrome-devtools-mcp"


def detected_targets() -> list[InstallTarget]:
    targets = [target for target in TARGETS if target.required or target.detected()]
    if targets:
        return targets
    return [TARGETS[0]]


def capability_summary(uv_ready: bool, python_version: tuple[int, int, int] | None, setup_ready: bool) -> str:
    python_ready = bool(python_version and python_version >= (3, 11))
    if uv_ready and python_ready and setup_ready:
        return "install + render ready"
    if uv_ready and python_ready:
        return "install ready, render will self-setup on first use"
    return "skill install works, render setup blocked until missing prerequisites are installed"


def print_environment_summary(home: Path, selected_targets: list[InstallTarget]) -> None:
    repo_scripts_dir = skill_dir() / "scripts"
    print()
    print("Detected install targets:")
    for target in TARGETS:
        cli_text = ", ".join(target.cli_names)
        detected = "yes" if target in selected_targets else "no"
        existing = "installed" if target.target(home).is_dir() else "not installed"
        print(f"  {target.label}: cli [{cli_text}] detected={detected}, target={existing}")

    if selected_targets == [TARGETS[0]] and not TARGETS[0].detected():
        print("  Fallback: no supported CLI detected, using ~/.agents/skills as the default shared location")

    print()
    print("Environment verification:")

    uv_ready, uv_text = uv_status()
    print(f"  uv: {uv_text}")

    python_cmd, python_version = find_python_command()
    if python_cmd and python_version:
        version_text = ".".join(str(part) for part in python_version)
        if python_version >= (3, 11):
            print(f"  python: available via {python_cmd} ({version_text}, meets >=3.11)")
        else:
            print(f"  python: available via {python_cmd} ({version_text}, requires >=3.11)")
    else:
        print("  python: missing")

    if render_venv_dir(repo_scripts_dir).is_dir():
        print("  render env: virtualenv present")
    else:
        print("  render env: virtualenv not created yet")

    marker_present = setup_marker(repo_scripts_dir).is_file()
    print(f"  render setup marker: {'present' if marker_present else 'missing'}")

    mcp_ready, mcp_text = chrome_devtools_mcp_status()
    print(f"  chrome-devtools-mcp: {mcp_text}")
    if not mcp_ready:
        print("    ↳ Recommended for fast PNG/video rendering (no Playwright install needed)")
        print("    ↳ Configure in Claude Code: add chrome-devtools-mcp to your MCP servers")

    print()
    print(f"Capability summary: {capability_summary(uv_ready, python_version, marker_present)}")
    if mcp_ready:
        print("  chrome-devtools-mcp: rendering will use real browser (fast, no install needed)")
    else:
        print("  chrome-devtools-mcp: not found — PNG/video rendering will fall back to Playwright")


def install_target(target: InstallTarget, home: Path) -> None:
    destination = target.target(home)
    if destination.is_dir():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        skill_dir(),
        destination,
        ignore=shutil.ignore_patterns(".venv", ".setup_complete", "__pycache__", ".DS_Store"),
    )
    print(f"✓ {target.label} -> {destination}")


def main() -> int:
    home = home_dir()
    selected_targets = detected_targets()

    print_environment_summary(home, selected_targets)

    print()
    print("Installing skill to:")
    for target in selected_targets:
        print(f"  - {target.label}")
    print()

    for target in selected_targets:
        install_target(target, home)

    print()
    print("Render setup is deferred.")
    print("The first PNG render will self-install its browser dependency if needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
