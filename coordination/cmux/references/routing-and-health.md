# cmux Routing and Health Reference

## Focus

```bash
cmux focus-pane --pane pane:2
cmux focus-panel --panel surface:7
```

Use focus commands only when the user needs the target selected. Layout
automation should usually leave focus alone.

## Move, Split Off, and Reorder

```bash
cmux move-surface --surface surface:7 --pane pane:2 --focus true
cmux move-surface --surface surface:7 --workspace workspace:2 --window window:1 --after surface:4
cmux split-off --surface surface:7 right
cmux reorder-surface --surface surface:7 --before surface:3
```

Surface handles remain the right target after moving or reordering. Verify with
`cmux list-pane-surfaces --pane <pane>` or `cmux identify --json`.

## Visual Confirmation

```bash
cmux trigger-flash --surface surface:7
cmux trigger-flash --workspace workspace:2
```

Use a flash after creating, moving, or selecting a surface when the user needs a
visual locator.

## Health Checks

```bash
cmux surface-health
cmux surface-health --workspace workspace:2
```

Run health checks when a surface may be hidden, detached, stale, or not attached
to the expected window before sending more routing commands.
