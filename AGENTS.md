# Agent Skills - Agent Context

This repository contains portable, public-safe agent skills. Keep private local
preferences, account details, publishing rules, credentials, and machine-specific
paths outside the repository.

## Structure

Category directories live at the repository root:

```text
content/
coordination/
git/
media/
project-management/
```

Each skill lives in its own directory with a `SKILL.md` entry point plus any
needed `scripts/`, `references/`, `assets/`, or `agents/` resources.

## Maintenance Rules

- Keep each skill self-contained, task-focused, and safe to publish.
- Keep trigger guidance explicit so agents know when to use the skill.
- Prefer reusable scripts or templates over long instructions that agents must
  retype.
- When adding, moving, renaming, or materially changing a skill, update
  `README.md` in the same change: repository layout, category listing, skill
  description, links, and usage example.
- Do not include sensitive values, private paths, identifiers, unpublished
  strategy, or local account assumptions.
- Do not commit local overlays such as `AGENTS.local.md` or `CLAUDE.local.md`.

## Verification

For documentation-only changes, review the rendered Markdown. For skill changes,
test the workflow manually or with the relevant bundled script.
