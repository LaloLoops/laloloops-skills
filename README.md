# Agent Skills

Portable, public-safe agent skills and supporting instructions.

## Install A Skill

Each skill is a directory with a `SKILL.md` entry point and optional bundled
resources such as `scripts/`, `references/`, `assets/`, and
`agents/openai.yaml`.

Copy the full skill directory into the target agent's skills directory. Do not
copy only `SKILL.md` when the skill has bundled resources.

```sh
mkdir -p "$AGENT_SKILLS_DIR"
cp -R skills/<category>/<skill-name> "$AGENT_SKILLS_DIR/"
```

Example:

```sh
mkdir -p "$HOME/.codex/skills"
cp -R skills/project-management/live-implementation-notes "$HOME/.codex/skills/"
```

For another agent, replace `$HOME/.codex/skills` with that agent's configured
skills directory. If an agent supports repository-local skills, you can also
point it at this repository or copy the desired skill folders into its local
skill path.

After installing, restart or reload the agent if it does not discover new
skills automatically.

This repository is intended to hold reusable skills, not private local agent
preferences or machine-specific configuration.

## Categories

### `content/`

Skills for turning development sessions, transcripts, or project activity into
journals, summaries, and reusable content ideas.

Included skills:

- [Journal Session Current](skills/content/journal-session-current/SKILL.md) -
  creates a journal summary and content ideas from the current conversation or
  provided notes.
- [Journal Session History](skills/content/journal-session-history/SKILL.md) -
  summarizes prior local agent session transcripts for a date or date range.

### `git/`

Skills for repository and pull request workflows.

Included skills:

- [PR Manage](skills/git/pr-manage/SKILL.md) - manages a pull request lifecycle
  through creation, review, CI follow-up, and merge readiness.

### `project-management/`

Skills for planning work, tracking implementation progress, and deciding what
to work on next.

Included skills:

- [Feature Planning Scaffold](skills/project-management/feature-planning-scaffold/SKILL.md) -
  creates a planning directory with an implementation plan and progress tracker.
- [Live Implementation Notes](skills/project-management/live-implementation-notes/SKILL.md) -
  keeps a live HTML implementation-notes file updated while work is happening.
- [Project Next Steps](skills/project-management/project-next-steps/SKILL.md) -
  reads repository evidence and recommends prioritized next work.

### `media/`

Skills for generated media assets and post-processing workflows.

Included skills:

- [Transparent Image Alpha](skills/media/transparent-image-alpha/SKILL.md) -
  converts flat chroma-key image generations into validated transparent
  PNG/WebP assets.

## Repository Layout

```text
skills/
├── content/
├── git/
├── media/
└── project-management/
```

See [skills/README.md](skills/README.md) for the category index.
