# cmux Settings Reference

## Discover Paths and Docs

```bash
cmux docs settings
cmux settings path
cmux settings
cmux settings cmux-json
cmux settings shortcuts
```

`cmux docs settings` is the first stop for current settings documentation,
schema links, raw resources, supported paths, and reload guidance.

## Edit Safely

1. Locate the active config with `cmux settings path`.
2. Back up `~/.config/cmux/cmux.json` to a timestamped `.bak` in the same
   directory before editing.
3. Edit only the requested keys.
4. Reload and verify:

   ```bash
   cmux reload-config
   ```

`cmux reload-config` reloads cmux app settings and Ghostty config without
requiring an app restart.

## Ownership Boundary

Use `cmux.json` for cmux-owned behavior:

- app appearance and sidebar behavior
- notifications and hooks
- browser and automation settings
- workspace colors
- cmux-owned shortcuts and actions

Use Ghostty config for terminal rendering:

- font and font size
- cursor style
- terminal theme
- scrollback
- background opacity
- background blur
