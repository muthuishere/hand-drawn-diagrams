# hand-drawn-diagrams

AI skill for turning ideas, notes, systems, and flows into hand-drawn diagrams — with a hosted edit URL, animated video, and PNG, all from a single prompt.

![Demo](assets/demo.gif)

## What this is

**hand-drawn-diagrams** is an AI skill (for Claude Code, Codex CLI, and compatible agents) that takes a natural language prompt and produces a hand-drawn diagram you can edit, animate, and share — without opening any app.

You describe what you want. The AI picks the right diagram type, draws it in Excalidraw's sketch style, validates the layout, and hands you a live hosted URL. From there you can edit it in a browser, watch it animate, download the source, or export a PNG.


## How it's different from using Excalidraw directly

| | Excalidraw | hand-drawn-diagrams |
|---|---|---|
| Starting point | Blank canvas, you draw | Natural language prompt |
| Diagram type | You decide | AI picks the right route (teaching, UX, architecture, funnel…) |
| Layout | You position everything | AI assigns non-overlapping coordinates |
| Animation | Manual or none | Auto-generated animation spec, renders in browser |
| Output | File on disk | Hosted edit URL + animated SVG + PNG on request |
| Workspace | You open the app | Files stay in `/tmp/` by default — workspace stays clean |

This skill is not a replacement for Excalidraw — it sits on top of it. Every diagram it produces is a standard `.excalidraw` file you can open, edit, and own.

## Best for

- students: study notes and exam revision maps
- teachers: lesson explainers and concept breakdowns
- architects: system and API flow diagrams
- builders: sequence diagrams and integration maps
- designers: UX flows and wireframes
- product: idea maps and feature flows
- sales: funnel and conversion visuals
- doctors: process and patient-facing explainers

## Output

Default delivery — no installs, fast path:

1. **Hosted edit URL** — open and edit in a browser, download the `.excalidraw` source. No local app needed.
2. **Animate URL** — click Animate in the editor to watch the diagram draw itself stroke by stroke.
3. **Animated SVG** — saved to your project when you ask for a video version. Plays in any browser, no app needed.
4. **PNG** — rendered on request via Chrome DevTools MCP (fast) or Playwright (fallback).

Source files (`.excalidraw`) go to `/tmp/hand-drawn-diagrams/` by default — your workspace stays clean.

## Install

macOS / Linux

```bash
git clone git@github.com:muthuishere/hand-drawn-diagrams.git
cd hand-drawn-diagrams
bash install.sh
```

Windows

```cmd
git clone git@github.com:muthuishere/hand-drawn-diagrams.git
cd hand-drawn-diagrams
install.cmd
```

The installer detects Claude Code and Agent CLI targets automatically and prints a capability summary.

## Uninstall

macOS / Linux

```bash
bash uninstall.sh
```

Windows

```cmd
uninstall.cmd
```

## Credits and acknowledgements

This skill stands on the shoulders of excellent open-source work:

- **[Excalidraw](https://excalidraw.com/)** — the open-source virtual whiteboard that powers the hand-drawn visual style and the hosted editor. All diagrams produced by this skill are standard Excalidraw files.
  GitHub: [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw)

- **[excalidraw-animate](https://github.com/dai-shi/excalidraw-animate)** by [@dai-shi](https://github.com/dai-shi) — the animation library that renders Excalidraw diagrams as SVGs that draw themselves stroke by stroke. The animated SVG output in this skill is powered by this library.

## License

MIT — see [LICENSE](LICENSE).
