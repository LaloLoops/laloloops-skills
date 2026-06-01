---
name: cmux
description: Operate the cmux CLI for deterministic control of cmux windows, workspaces, panes, terminal/browser surfaces, focus, moves, reorders, split-off flows, visual flashes, surface health checks, and safe cmux-owned settings reloads. Use when managing or automating cmux layouts, routing work into the caller workspace, inspecting cmux topology, opening terminal or browser surfaces, or changing cmux CLI/app settings.
---

# cmux CLI

Use `cmux` as the control plane for the running cmux app. Start from the caller
context, use stable handles, inspect before changing topology, and prefer
additive changes over disruptive ones.

## Core Workflow

1. Confirm the CLI is available when the session has not used it yet:

   ```bash
   command -v cmux
   cmux --help
   ```

2. Identify the current caller context before routing work:

   ```bash
   cmux identify --json
   cmux current-workspace --json
   ```

3. Inspect the relevant topology before making changes:

   ```bash
   cmux list-windows
   cmux list-workspaces
   cmux list-panes
   cmux list-pane-surfaces --pane pane:1
   ```

4. Make the smallest layout change that satisfies the request. Use short
   handles such as `window:1`, `workspace:2`, `pane:3`, and `surface:4`.

5. Verify the result with `cmux identify --json`, list commands, or
   `cmux surface-health`, then use `cmux trigger-flash` when a visible cue helps
   the user locate the target surface.

## Targeting Rules

- Use JSON output for scripts, state comparisons, or any workflow where parsing
  matters.
- Anchor automation to the caller workspace unless the user explicitly asks to
  affect another window or workspace.
- Treat close, move, and reorder commands as topology changes: list first, act
  on explicit handles, then verify.
- Keep layout commands focus-neutral unless changing focus is the point of the
  request. Pass `--focus true` only when the created or moved surface should
  become active.
- Prefer creating a new pane or surface over repurposing an existing one when
  there is any ambiguity.

## Common Operations

Create and focus:

```bash
cmux new-window
cmux new-workspace
cmux new-split right --panel pane:1
cmux new-surface --type terminal --pane pane:1
cmux new-surface --type browser --pane pane:1 --url https://example.com
cmux focus-pane --pane pane:2
cmux focus-panel --panel surface:7
```

Move and reorder:

```bash
cmux move-surface --surface surface:7 --pane pane:2 --focus true
cmux move-surface --surface surface:7 --workspace workspace:2 --window window:1
cmux split-off --surface surface:7 right
cmux reorder-surface --surface surface:7 --before surface:3
cmux reorder-workspace --workspace workspace:4 --before workspace:2
```

Visual confirmation and health:

```bash
cmux trigger-flash --surface surface:7
cmux trigger-flash --workspace workspace:2
cmux surface-health
cmux surface-health --workspace workspace:2
```

## Settings

Before changing cmux-owned settings, ask the CLI for the current docs and paths:

```bash
cmux docs settings
cmux settings path
```

cmux app settings belong in `~/.config/cmux/cmux.json`. Back up that file to a
timestamped `.bak` next to it before editing, then reload:

```bash
cmux reload-config
```

Use cmux settings for app behavior, sidebar, notifications, browser behavior,
automation, workspace colors, and cmux-owned shortcuts. Terminal rendering
settings such as font, cursor, theme, scrollback, opacity, and blur belong in
Ghostty config, not `cmux.json`.

## References

Load only the reference needed for the current task:

| Reference | Use |
| --- | --- |
| [references/topology.md](references/topology.md) | Handles, identifying caller context, windows, workspaces, panes, and surfaces. |
| [references/routing-and-health.md](references/routing-and-health.md) | Focus, move, split-off, reorder, flash, and surface health checks. |
| [references/settings.md](references/settings.md) | Safe cmux settings discovery, backup, edit, and reload flow. |

For upstream changes, check `cmux --help`, `cmux docs settings`, and the cmux
skills docs at <https://cmux.com/docs/skills>.
