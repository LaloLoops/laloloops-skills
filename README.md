# Agent Skills

Portable, public-safe agent skills and supporting resources.

Each skill is a directory with a `SKILL.md` entry point and optional bundled
resources such as `scripts/`, `references/`, `assets/`, and
`agents/openai.yaml`. Category directories live directly at the repository root.

## Install A Skill

Copy the full skill directory into the target agent's skills directory. Do not
copy only `SKILL.md` when the skill has bundled resources.

```sh
mkdir -p "$AGENT_SKILLS_DIR"
cp -R <category>/<skill-name> "$AGENT_SKILLS_DIR/"
```

Example:

```sh
mkdir -p "$HOME/.codex/skills"
cp -R coordination/agent-comm "$HOME/.codex/skills/"
```

For another agent, replace `$HOME/.codex/skills` with that agent's configured
skills directory. If an agent supports repository-local skills, you can also
point it at this repository or copy the desired skill folders into its local
skill path.

After installing, restart or reload the agent if it does not discover new
skills automatically.

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

### `content/`

Skills for turning development sessions, transcripts, or project activity into
journals, summaries, and reusable content ideas.

- [Journal Session Current](content/journal-session-current/SKILL.md): creates a
  factual journal summary and content ideas from the current conversation or
  provided notes.
  Example: `Use journal-session-current to summarize this session and give me 3 content ideas.`

- [Journal Session History](content/journal-session-history/SKILL.md): scans
  local agent session transcripts for a date or range and summarizes what
  happened.
  Example: `Use journal-session-history to summarize yesterday's agent work from local transcripts.`

### `coordination/`

Skills for coordinating multiple agent sessions or handoffs through shared,
inspectable state.

- [Agent Comm](coordination/agent-comm/SKILL.md): coordinates two or more agent
  sessions through `.agent-comm/` files, status updates, compact state, and an
  explicit approval gate before risky actions.
  Example: `Use agent-comm so one session prepares the deploy while another waits for approval and reports status.`

### `git/`

Skills for repository, pull request, review, CI, and merge workflows.

- [PR Manage](git/pr-manage/SKILL.md): owns a pull request lifecycle from the
  current branch through PR creation, review requests, CI fixes, feedback
  handling, and merge when ready.
  Example: `Use pr-manage to open a PR for this branch, request review, monitor CI, and merge when approved.`

### `media/`

Skills for generated media assets and post-processing workflows.

- [Transparent Image Alpha](media/transparent-image-alpha/SKILL.md): turns a
  flat chroma-key generated image into a validated transparent PNG or WebP using
  the bundled helper script.
  Example: `Use transparent-image-alpha to make this generated sticker a real transparent PNG.`

### `project-management/`

Skills for planning work, tracking implementation progress, and deciding what
to work on next.

- [Feature Planning Scaffold](project-management/feature-planning-scaffold/SKILL.md):
  creates a repository-local planning directory with an implementation plan and
  progress tracker for a feature, bug fix, refactor, or investigation.
  Example: `Use feature-planning-scaffold to create a plan for the billing retry refactor.`

- [Live Implementation Notes](project-management/live-implementation-notes/SKILL.md):
  maintains a timestamped implementation-notes HTML file outside the repository
  while coding work is happening.
  Example: `Use live-implementation-notes while implementing this so I can inspect progress as you work.`

- [Project Next Steps](project-management/project-next-steps/SKILL.md): performs
  a read-only project sweep and recommends prioritized next work from issues,
  PRs, commits, planning files, and docs.
  Example: `Use project-next-steps to tell me what we should tackle next, with evidence.`

## Public-Safe Scope

This repository is intended to hold reusable skills, not private local agent
preferences or machine-specific configuration. If a skill needs local setup,
document the expected environment variables or external files without committing
real values.
