# Contributing

This is an agentic skill (`SKILL.md`) plus the Python scripts it drives (`scripts/`), not
a conventional app — so "contributing" here mostly means changing either the skill's
routing logic (`steps/`) or the rendering/validation code it calls into.

## Repo shape

- `SKILL.md` — the entry point an agent reads. Changes here affect every agent that has
  this skill installed, so keep edits small and test the three-step flow end to end
  (`steps/step-01-route.md` → `step-02-draw.md` → `step-03-validate.md`) before opening a PR.
- `scripts/` — a `uv`-managed Python project (`scripts/pyproject.toml`) that does the real
  work: rendering, validating, hosting, and animating `.excalidraw` files.
- `.github/workflows/skill-review.yml` — runs automatically on any PR touching `SKILL.md`.
  Let it finish before asking for a look.

## Running the tests

```bash
cd scripts
uv run pytest -m "not slow"     # fast suite, no Playwright/Chromium needed — verify this passes before opening a PR
uv run pytest                   # full suite, includes Playwright-backed render tests
```

If you're touching `validate_excalidraw.py`, `render_excalidraw.py`, or anything that
opens a browser, run the full suite (`slow` tests included) — the fast suite skips exactly
the code paths those files exercise.

## What a good PR looks like

- **Validate before you claim it works.** `scripts/validate_excalidraw.py` exists because
  a broken or empty `.excalidraw` file failing silently is the worst outcome this skill can
  produce — SKILL.md says "always validate before generating URLs, never share an empty
  diagram" for exactly that reason. A change that can produce an invalid diagram needs a
  test proving it can't, not a claim that it won't.
- **Keep the skill monochrome-sketch by default.** Color is opt-in for page-mockup-style
  output only — if your change affects styling defaults, say so explicitly in the PR.
- **Small, single-purpose.** A routing change in `steps/` and a rendering change in
  `scripts/` are two PRs, not one, unless one genuinely can't ship without the other.

## Filing an issue

If a diagram came out wrong, attach the actual `.excalidraw` file (or the prompt that
produced it) rather than a screenshot alone — most bugs here are in how the AI or the
renderer interpreted specific content, and the source file is what actually reproduces it.
