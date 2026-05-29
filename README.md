# LaloLoops Agent Skills

Portable, public-safe agent skills and supporting resources.

Each skill is a directory with a `SKILL.md` entry point and optional bundled
resources such as `scripts/`, `references/`, `assets/`, and
`agents/openai.yaml`. Category directories live directly at the repository root.

## Install For Claude Code

Copy the full skill directory into Claude Code's skills directory. Do not copy
only `SKILL.md` when the skill has bundled resources.

Use personal installation when you want the skill available in every Claude Code
project:

```sh
mkdir -p "$HOME/.claude/skills"
cp -R <category>/<skill-name> "$HOME/.claude/skills/"
```

Example:

```sh
mkdir -p "$HOME/.claude/skills"
cp -R coordination/agent-comm "$HOME/.claude/skills/"
```

Use project installation when you want the skill available only in one project:

```sh
mkdir -p /path/to/project/.claude/skills
cp -R <category>/<skill-name> /path/to/project/.claude/skills/
```

To install every skill in this repository as personal Claude Code skills:

```sh
mkdir -p "$HOME/.claude/skills"
for skill in content/* coordination/* git/* media/* project-management/*; do
  [ -d "$skill" ] && cp -R "$skill" "$HOME/.claude/skills/"
done
```

Claude Code uses the installed directory name as the slash command. For example,
after installing `coordination/agent-comm`, invoke it directly with
`/agent-comm` or let Claude load it automatically when your request matches the
skill description.

Claude Code watches existing skill directories for changes. If `~/.claude/skills`
or `.claude/skills` did not exist when the current Claude Code session started,
restart Claude Code once so it begins watching the new directory.

## Install For Codex

Copy the full skill directory into Codex's skills directory. Do not copy only
`SKILL.md` when the skill has bundled resources.

Use personal installation when you want the skill available in every Codex
session:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R <category>/<skill-name> "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Example:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R media/ascii-diagram "${CODEX_HOME:-$HOME/.codex}/skills/"
```

To install every skill in this repository as personal Codex skills:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
for skill in content/* coordination/* git/* media/* project-management/*; do
  [ -d "$skill" ] && cp -R "$skill" "${CODEX_HOME:-$HOME/.codex}/skills/"
done
```

Restart Codex after adding a new global skill so the next session discovers it.

## Repository Layout

```text
.
├── content/
├── coordination/
├── git/
├── media/
└── project-management/
```

## Skill Index

Skills are prompt-driven. The "parameters" below are the useful details to put
after the slash command or include in the request. Claude Code or Codex may also
load a skill automatically when the request matches its description.

Jump to a category or skill:

- [`content/`](#content)
  - [Journal Session Current](#journal-session-current)
  - [Social Post Teardown](#social-post-teardown)
  - [Journal Session History](#journal-session-history)
- [`coordination/`](#coordination)
  - [Agent Comm](#agent-comm)
  - [Agent Session Launcher](#agent-session-launcher)
- [`git/`](#git)
  - [PR Manage](#pr-manage)
- [`media/`](#media)
  - [ASCII Diagram](#ascii-diagram)
  - [Transparent Image Alpha](#transparent-image-alpha)
- [`project-management/`](#project-management)
  - [Feature Planning Scaffold](#feature-planning-scaffold)
  - [Live Implementation Notes](#live-implementation-notes)
  - [Project Next Steps](#project-next-steps)

### `content/`

Skills for turning development sessions, transcripts, or project activity into
journals, summaries, and reusable content ideas.

#### [Journal Session Current](content/journal-session-current/SKILL.md)

Creates a factual journal summary and reusable content ideas from the current
conversation or provided notes.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `mode` | `journal`, `quick`, `ideas`, or a custom output hint. |
| `source` | Current conversation by default, or pasted notes/history digest. |
| `focus` | Optional topic, audience, lesson, or content angle to bias ideas toward. |
| `voice` | Optional style guide or tone request. Defaults to neutral and practical. |

Produces: journal summary, key decisions, open threads, content ideas, reusable
notes, and follow-up questions. In `journal` mode it outputs only the factual
record.

Example request:

```text
/journal-session-current mode=quick focus="agent coordination"
Summarize this session and give me 3 content ideas.
```

Example output shape:

```markdown
# Journal Session Current

Date: 2026-05-21
Session focus: Renamed and reorganized a reusable agent skill collection.

## 1. Journal Summary
- ...

## 2. Content Ideas
1. ...
```

#### [Social Post Teardown](content/social-post-teardown/SKILL.md)

Breaks down a single short-form social post into its big idea, structure, word
choice, engagement drivers, and psychological tactics, then turns the pattern
into a step-by-step replication template the user can apply to their own ideas.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `post` | Required. Full text of the social post being analyzed. |
| `platform` | Optional. `twitter`, `linkedin`, `instagram`, `tiktok`, `threads`, `reddit`, or similar. |
| `context` | Optional. Author, audience, niche, or reported engagement numbers. |
| `replicate_topic` | Optional. The user's own idea to express in the same style. |
| `voice` | Optional. Tone or brand constraints to respect in the worked example. |
| `depth` | `standard` by default. `quick` for sections 1-4 plus template. `deep` adds line-by-line annotation. |

Produces: big-idea summary, structure map, word-choice analysis, engagement
drivers, named psychological tactics with quoted spans, a reusable skeleton
template, and an optional worked example in the user's voice.

Example request:

```text
/social-post-teardown platform=linkedin depth=standard
Tear this post down and show me how to write one like it.

<paste the post>
```

#### [Journal Session History](content/journal-session-history/SKILL.md)

Scans local Codex, Claude Code, and Hermes agent session transcripts for a date
or range, then summarizes what happened without dumping raw transcript soup into
your lap.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `date` | Single date as `YYYY-MM-DD`. Defaults to today's local date. |
| `date_from`, `date_to` | Inclusive date range. |
| `source` | `all`, `codex`, `claude`, or `hermes`. |
| `project_filter` | Optional substring to narrow Claude project paths. |
| `max_items` | Optional cap when the transcript digest is too large. |
| `format` | `markdown` by default; `json` when structured analysis is easier. |
| `include_excerpts` | Include compact raw excerpts only when explicitly needed. |

Bundled script:

```sh
python3 content/journal-session-history/scripts/journal_history.py \
  --date 2026-05-21 \
  --source all
```

Produces: executive summary, story briefs, lessons, and draft content starters
grounded in transcript evidence.

Example request:

```text
/journal-session-history date=2026-05-20 source=claude project_filter=laloloops
Summarize the useful product/dev work from that day.
```

### `coordination/`

Skills for coordinating multiple agent sessions or handoffs through shared,
inspectable state.

#### [Agent Comm](coordination/agent-comm/SKILL.md)

Coordinates two or more agent sessions through a shared `.agent-comm/` mailbox,
status log, compact state file, and explicit approval gate before risky actions.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `workspace` | Repository or filesystem path both sessions can access. |
| `roles` | Which session coordinates and which executes, verifies, deploys, or observes. |
| `phases` | Custom phase names, allowed actions, standby behavior, and terminal states. |
| `approval_action` | Exact risky action that requires human approval. |
| `approval_phrase` | Human-facing phrase or condition that unlocks the action. |
| `poll_interval` | How often the executor should reread `state.json` while standing by. |
| `redaction_rules` | Any project-specific data that must not appear in files or chat. |

Produces:

```text
.agent-comm/
├── inbox.md
├── status.md
└── state.json
```

Example request:

```text
/agent-comm workspace=. approval_action="production deploy"
Set up one executor to prepare the deploy, stop at standby, and wait for my approval.
```

#### [Agent Session Launcher](coordination/agent-session-launcher/SKILL.md)

Launches Claude Code or Codex in a chosen repository, usually inside tmux,
after asking a short pre-launch checklist for agent, session mode, permission
posture, workspace, and task prompt.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `agent` | `claude` or `codex`. Ask if not specified. |
| `mode` | `interactive-tmux` or `inline`. Ask if not specified. |
| `permissions` | `normal`, `more-automatic`, or `skip-permissions`. Make the trade-off explicit. |
| `workspace` | Repository or folder path to launch inside. |
| `prompt` | Exact task to run in the launched agent session. |
| `artifact` | Optional file output the launched agent should produce. |
| `gui_terminal` | Optional. Only if the user explicitly wants a GUI terminal window opened. |

Produces: a launched agent session, a verified running/waiting/completed state,
and an attach command such as `tmux attach -t <session>`.

Example request:

```text
/agent-session-launcher agent=claude mode=interactive-tmux permissions=normal workspace=.
Start Claude Code in tmux, give it the prompt below, and tell me how to reattach.
```

### `git/`

Skills for repository, pull request, review, CI, and merge workflows.

#### [PR Manage](git/pr-manage/SKILL.md)

Owns a pull request lifecycle from the current branch through PR creation,
review requests, CI fixes, feedback handling, and merge when ready.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `base` | Target branch. Defaults to the repository default branch. |
| `draft` | Whether to open as draft or ready for review. |
| `reviewer` | Optional reviewer account or documented review trigger. |
| `merge_when_ready` | Whether the agent should merge after checks and review pass. |
| `merge_method` | Optional preference: squash, merge commit, or rebase. |
| `GH_CMD` | Optional environment override for the GitHub CLI command. |

Produces: PR URL, review/check status, commits for fixes when needed, merge
result or clear blocker.

Example request:

```text
/pr-manage base=main reviewer=@reviewer merge_when_ready=true
Open a PR for this branch, request review, fix failing checks, and merge once approved.
```

### `media/`

Skills for generated media assets and post-processing workflows.

#### [ASCII Diagram](media/ascii-diagram/SKILL.md)

Renders tidy ASCII or Unicode box-and-arrow diagrams from Graph::Easy DSL using
the bundled wrapper script.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `diagram` | Topology, architecture, flowchart, dependency graph, or state-machine content to render. |
| `format` | Optional output format: `boxart` by default, `ascii` for 7-bit output, or `svg` / `graphviz` if requested. |
| `flow` | Optional layout direction: `east`, `west`, `down`, or `up`. |
| `labels` | Optional edge labels, protocol names, step numbers, or channel distinctions. |

Bundled script:

```sh
media/ascii-diagram/scripts/graph-easy.sh <<'EOF'
graph { flow: east; }
[ Client ] -- request --> [ API ] -- query --> [ Database ]
EOF
```

Produces: rendered diagram output suitable for fenced Markdown code blocks,
plus the Graph::Easy DSL if useful for later edits.

Example request:

```text
/ascii-diagram format=boxart flow=down
Draw the signup flow from landing page to account activation.
```

#### [Transparent Image Alpha](media/transparent-image-alpha/SKILL.md)

Turns a flat chroma-key generated image into a validated transparent PNG or WebP
using the bundled helper script.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `subject` | What the generated asset should contain. |
| `style` | Optional art direction, composition, size, or padding. |
| `key` | Chroma color. Defaults to `#00ff00`; use `#ff00ff` when green appears in the subject. |
| `input` | Source keyed image path if the image already exists. |
| `out` | Final `.png` or `.webp` path. |
| `edge_contract` | Optional 1 px matte contraction for color fringes. |
| `force` | Overwrite output only when explicitly requested. |

Bundled script:

```sh
python3 media/transparent-image-alpha/scripts/make_alpha_from_chroma.py \
  --input source-keyed.png \
  --out final-transparent.png \
  --key '#00ff00'
```

Produces: transparent PNG/WebP, source path, key color, and validation summary.

Example request:

```text
/transparent-image-alpha subject="a tiny robot sticker" out=robot.png key=#00ff00
Generate it on a flat key background, remove the key, and validate the alpha.
```

### `project-management/`

Skills for planning work, tracking implementation progress, and deciding what
to work on next.

#### [Feature Planning Scaffold](project-management/feature-planning-scaffold/SKILL.md)

Creates a repository-local planning directory with an implementation plan and
progress tracker for a feature, bug fix, refactor, or investigation.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `title` | Work item title or short description. |
| `reference` | Optional issue, ticket, PR, or external reference. |
| `planning_root` | Directory root. Defaults to `planning/`. |
| `scope` | Optional in-scope and out-of-scope hints. |
| `priority` | Optional priority if the project tracks it. |

Produces:

```text
planning/<date>_<slug>/
├── 000_<slug>_implementation_plan.md
└── PROGRESS.md
```

Example request:

```text
/feature-planning-scaffold title="billing retry refactor" reference="#123"
Create a plan with scope, phases, risks, and verification gates.
```

#### [Live Implementation Notes](project-management/live-implementation-notes/SKILL.md)

Maintains a timestamped implementation-notes HTML file outside the repository
while coding work is happening.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `task` | What implementation work should be tracked. |
| `scope` | Optional boundaries, assumptions, or known risks. |
| `notes_path` | Optional existing notes file. Defaults to a new temp HTML file. |
| `update_triggers` | Optional events that should force a notes update. |

Produces: a self-contained HTML notes file with overview, status, decisions,
changes, tradeoffs, verification, and handoff sections.

Example request:

```text
/live-implementation-notes task="refactor the export flow"
Track decisions, changed files, verification, and any handoff notes while you work.
```

Example output:

```text
Created live implementation notes: /tmp/implementation-notes-20260521-143000-a1b2c3.html
```

#### [Project Next Steps](project-management/project-next-steps/SKILL.md)

Performs a read-only project sweep and recommends prioritized next work from
issues, PRs, commits, planning files, and docs.

Inputs:

| Parameter | Meaning |
| --- | --- |
| `focus` | Optional filter such as `bug`, `ci`, `docs`, `ui`, issue number, PR, or keyword. |
| `evidence_sources` | Optional hint to inspect issues, PRs, planning files, commits, or docs. |
| `candidate_count` | Desired number of recommendations. Defaults to 3-5. |
| `size_bias` | Optional preference for small wins, in-flight work, or larger roadmap items. |

Produces: project snapshot, flagged concerns, ranked recommendations, evidence,
blockers, suggested action, and rough size.

Example request:

```text
/project-next-steps focus=ci candidate_count=3
Tell me what we should tackle next and cite the evidence.
```

Example output shape:

```markdown
# Project Next Steps - 2026-05-21

## Snapshot
- Branch: main (clean)

## Recommended Next Steps
### 1. Fix failing export check - ci - score 8
- **Evidence**: PR #42, failing workflow link
- **Suggested action**: fix directly
```

## Public-Safe Scope

This repository is intended to hold reusable skills, not private local agent
preferences or machine-specific configuration. If a skill needs local setup,
document the expected environment variables or external files without committing
real values.
