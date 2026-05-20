# Agent Skills - Agent Context

This repository contains reusable agent skills and supporting instructions.
Treat it as a portable skills collection: files should be useful outside the
author's local machine and safe to publish.

Keep this file public-safe. Machine-specific preferences, account details,
commit-author identity, and publishing rules belong in local configuration
outside the repository.

## Repository Layout

Current layout:

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
└── skills/
    ├── content/
    ├── git/
    ├── media/
    └── project-management/
```

Add skill directories as the collection grows. A typical skill should have its
own directory with a `SKILL.md` entry point plus any scripts, references, or
assets it needs.

## Skill Authoring Rules

- Make each skill self-contained and task-focused.
- Keep trigger guidance explicit so agents know when to use the skill.
- Prefer reusable scripts or templates over long instructions that agents must
  retype.
- Keep examples generic unless the skill is intentionally specialized.
- Do not include sensitive values, private paths, identifiers, unpublished
  strategy, or local account assumptions.
- If a skill needs local configuration, document the expected environment
  variables or external files without committing real values.

## Cross-Agent Setup

- `AGENTS.md` is the shared public guidance.
- `CLAUDE.md` imports `AGENTS.md` for Claude Code compatibility.
- Local preferences should live outside this repository.
- Do not commit local overlays such as `AGENTS.local.md` or `CLAUDE.local.md`.

## Verification

For documentation-only changes, review the rendered Markdown. For skill changes,
test the workflow manually or with the relevant script before committing.
