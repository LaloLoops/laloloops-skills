---
name: feature-planning-scaffold
description: Scaffold a project planning directory with an implementation plan, progress tracker, and optional issue reference. Use when starting a new feature, bug fix, refactor, or investigation that benefits from a written plan before code changes.
---

# Feature Planning Scaffold

Create a compact planning directory for a new work item. Keep the output generic
and repository-local. Do not assume a particular language, framework, product,
or issue tracker unless the current repository clearly establishes one.

## Workflow

1. Parse the user's request for:
   - Work item title or short description.
   - Optional issue, ticket, or PR reference.
   - Optional planning directory root. Default to `planning/`.
2. If the title is missing or too vague, ask one concise question before
   creating files.
3. Derive:
   - `slug`: lowercase snake_case, 3-6 meaningful words when possible.
   - `date_prefix`: today's local date as `YYYYMMDD`.
   - `title`: title case for headings.
4. Check for same-day directory collisions:

```bash
ls -d planning/${date_prefix}* 2>/dev/null
```

If a same-day directory exists, append the next numeric suffix after the date,
such as `20260518_2_slug`.

5. Create:
   - `planning/<date>_<slug>/000_<slug>_implementation_plan.md`
   - `planning/<date>_<slug>/PROGRESS.md`

Use `apply_patch` for file creation when working inside Codex.

## Implementation Plan Template

Use this structure for `000_<slug>_implementation_plan.md`:

```markdown
# <Title> Implementation Plan

**Date**: <YYYY-MM-DD>
**Status**: Planning
**Priority**: TBD
**Reference**: <issue/ticket/PR or none>

## Goal

<!-- What this work achieves and why it matters. -->

## Scope

### In Scope

<!-- Concrete included work. -->

### Out Of Scope

<!-- Explicit exclusions. -->

## Current State

<!-- How the relevant system works today. Cite files when known. -->

## Design Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| | | |

## Implementation Phases

### Phase 1: <Name>

**Objective**: <!-- What this phase achieves. -->

**Target Files**:

- `path/to/file`

**Changes**:

<!-- Specific edits or behavior changes. -->

## Verification

| Change | Check | Status |
| --- | --- | --- |
| | | Pending |

## Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| | Low/Medium/High | Low/Medium/High | |
```

## Progress Template

Use this structure for `PROGRESS.md`:

```markdown
# Progress: <Title>

**Created**: <YYYY-MM-DD>
**Updated**: <YYYY-MM-DD>
**Status**: Planning
**Plan**: `000_<slug>_implementation_plan.md`
**Reference**: <issue/ticket/PR or none>

## Overview

<!-- 1-3 sentence summary of the work. -->

## Implementation Steps

| Step | Description | Status |
| --- | --- | --- |
| 1 | Fill in implementation plan | Pending |
| 2 | Begin implementation | Pending |

## Quality Gates

List only checks that exist in the repository. Examples:

- `<build command>` - Pending
- `<test command>` - Pending
- `<lint or format command>` - Pending

## Files Created

| File | Purpose |
| --- | --- |

## Files Modified

| File | Changes |
| --- | --- |

## Documents

| File | Description |
| --- | --- |
| `000_<slug>_implementation_plan.md` | Implementation plan |
| `PROGRESS.md` | Execution tracker |

## Activity Log

| Date | Update | Next |
| --- | --- | --- |
| <YYYY-MM-DD> | Created planning directory and initial files | Fill in plan details |
```

## Reporting

After creating the files, report:

- Planning directory path.
- Files created.
- Any assumptions made, especially if no issue reference or quality gates were
  known.
- The next concrete planning step.
