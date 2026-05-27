---
name: ascii-diagram
description: >-
  Generate clean ASCII / Unicode diagrams (box-and-arrow topology, architecture,
  flowcharts, dependency graphs, state machines) by rendering a Graph::Easy DSL
  with the local `graph-easy` CLI. Use whenever the user asks for an ASCII art
  diagram, a topology/architecture diagram, a flow diagram, or wants a hand-drawn
  diagram replaced with a tidy generated one. Not for image output (PNG/SVG) or
  for true UML sequence diagrams with lifelines.
---

# ASCII / Unicode diagrams via Graph::Easy

Render diagrams from a small text DSL instead of hand-drawing ASCII. The wrapper
script handles the install path; you only write the DSL and pick a format.

## How to render

Pipe Graph::Easy DSL into the wrapper (defaults to Unicode `boxart`):

```bash
media/ascii-diagram/scripts/graph-easy.sh <<'EOF'
[ A ] -- label --> [ B ]
EOF
```

From a Codex global install, locate the wrapper with:

```bash
"${CODEX_HOME:-$HOME/.codex}/skills/ascii-diagram/scripts/graph-easy.sh" <<'EOF'
[ A ] -- label --> [ B ]
EOF
```

From an installed Claude Code skill, use
`"$CLAUDE_SKILL_DIR/scripts/graph-easy.sh"`.

Output formats (pass `--as=`):
- `--as=boxart`  Unicode box-drawing (default, best looking)
- `--as=ascii`   pure 7-bit ASCII (use when the target is ASCII-only)
- `--as=svg` / `--as=graphviz`  hand off to other renderers if asked

## DSL cheat-sheet

```
graph { flow: east; }          # layout direction: east|west|down|up (default east)

[ Node ]                       # a node; spaces allowed inside the brackets
[ A ] --> [ B ]                # directed edge
[ A ] -- text --> [ B ]        # edge with a label
[ A ] ==> [ B ]                # bold/double edge (good for a distinct channel, e.g. gRPC)
[ A ] - - > [ B ]              # dashed edge
[ A ] <--> [ B ]               # bidirectional
[ A ] --> [ B ] --> [ C ]      # chains
( Group: [ A ] [ B ] )         # draw a labelled box around a subgraph

[ A ] { shape: rounded; }      # node attributes (shape: box|rounded|circle|none ...)
[ A ] { label: "Two\nLines"; } # multi-line label via an explicit label attribute
graph { flow: down; }          # top-to-bottom flow for step-by-step flows
```

## Authoring tips

- Keep node names short and stable; if you need multi-line text use the
  `label:` attribute (raw `\n` inside `[ ... ]` is treated literally).
- Do NOT put `{`, `}`, or `=` raw inside node/edge labels — they are DSL
  metacharacters and the parser will reject the line. Reword (e.g. write
  `GET file` instead of `GET /v1/files/{id}`, `set` instead of `=`).
- Prefer `flow: east` for topology, `flow: down` for ordered/step flows.
- Number steps in edge or node labels (`1: CreateSession`) to convey sequence,
  since this is a graph renderer, not a swimlane sequence-diagram tool.
- Use `==>` to visually separate a different protocol/channel from `-->`.
- Always show the rendered output to the user; when writing it into a markdown
  file, wrap it in a fenced code block so the alignment is preserved.

## Local dependency

```bash
brew install cpanminus
cpanm -n -l "$HOME/.local/perl5" Graph::Easy   # binary: ~/.local/perl5/bin/graph-easy
```
