# cmux Topology Reference

## Handles

Most topology commands accept stable short handles:

| Entity | Example |
| --- | --- |
| Window | `window:1` |
| Workspace | `workspace:2` |
| Pane | `pane:3` |
| Surface | `surface:4` |

UUIDs can be used when a command or script needs durable identity across list
output formats. Prefer short handles for interactive CLI work.

## Caller Context

Use these before changing layout:

```bash
cmux identify --json
cmux current-window
cmux current-workspace --json
```

When an operation must be anchored to a known place, pass the workspace or
surface explicitly:

```bash
cmux identify --workspace workspace:2
cmux identify --workspace workspace:2 --surface surface:8
```

## Inspect

```bash
cmux list-windows
cmux list-workspaces
cmux list-panes
cmux list-pane-surfaces --pane pane:1
```

## Window and Workspace Lifecycle

```bash
cmux new-window
cmux focus-window --window window:2
cmux close-window --window window:2

cmux new-workspace
cmux select-workspace --workspace workspace:4
cmux close-workspace --workspace workspace:4
cmux reorder-workspace --workspace workspace:4 --before workspace:2
cmux move-workspace-to-window --workspace workspace:4 --window window:1
```

Close commands are destructive to the user's layout. Re-list, confirm the handle,
and prefer asking for confirmation when the target is ambiguous.

## Pane and Surface Creation

```bash
cmux new-split right --panel pane:1
cmux new-surface --type terminal --pane pane:1
cmux new-surface --type browser --pane pane:1 --url https://example.com
```

Common split directions are `left`, `right`, `up`, and `down`. Use the existing
pane handle as the anchor for the split.
