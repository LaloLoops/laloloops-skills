---
name: project-next-steps
description: Produce prioritized, evidence-based recommendations for what to work on next by reading issues, pull requests, recent commits, planning progress files, and repository documentation. Use when the user asks what to tackle next or wants a project-state sweep before choosing work.
---

# Project Next Steps

Recommend what to work on next from verified project evidence. This is a
read-only analysis skill: do not edit files, create issues, comment on PRs,
commit, push, or start implementation unless the user explicitly asks after
the recommendation.

## Focus

Interpret the user's hint as a filter or weighting signal:

| Hint | Interpretation |
| --- | --- |
| empty | Full sweep across active work |
| `bug`, `regression`, `ci`, `testing` | Prioritize correctness, failed checks, and verification gaps |
| `ui`, `docs`, `performance`, `refactor` | Prioritize that area when ranking candidates |
| issue, PR, ticket, or keyword | Treat it as the primary search focus |

Ask one concise clarifying question only when the hint is genuinely ambiguous.

## Evidence Collection

Gather independent evidence in parallel when possible. Use the repository's
available tools and skip sources that are unavailable.

### Local Git State

```bash
git status --short
git branch --show-current
git log --oneline --decorate -30
git log --oneline @{upstream}..HEAD 2>/dev/null || true
```

Capture branch, dirty files, ahead/behind signal, and recent commit subjects.

### Pull Requests And Issues

Use the configured repository CLI or connector. For GitHub repositories, these
commands are reasonable read-only defaults:

```bash
gh issue list --state open --limit 50 --json number,title,labels,assignees,updatedAt
gh issue list --state closed --limit 15 --json number,title,closedAt,labels
gh pr list --state open --limit 20 --json number,title,headRefName,isDraft,updatedAt,reviewDecision,mergeStateStatus
gh pr list --state merged --limit 15 --json number,title,mergedAt,headRefName
```

If the repository uses another host or a wrapper command, use that instead and
keep the queries read-only.

### Planning Files

If `planning/` exists, inspect recent `PROGRESS.md` files first:

```bash
find planning -maxdepth 3 -name PROGRESS.md 2>/dev/null | sort -r | head -20
```

For each relevant progress file, capture:

- Title from the first heading.
- Status from a `Status` line if present.
- Updated date if present.
- Pending, in-progress, or blocked steps.
- Last activity-log row and its next action.

A stale progress file with pending work is a strong resume candidate.

### Documentation

Read only targeted sections needed to verify a candidate. Good sources often
include:

- `README.md`
- `AGENTS.md`
- `docs/`
- Architecture, roadmap, testing, or contribution docs when present.

Do not bulk-read documentation without a candidate question.

## Synthesis

Classify evidence into these buckets:

| Bucket | Signal |
| --- | --- |
| Shipped recently | Merged PRs, closed issues, recent main-branch commits |
| In flight | Open PRs, dirty working tree, in-progress planning files |
| Stalled | Draft PRs, blocked progress files, stale pending plans |
| Planned | Open issues or planning docs with no active PR |
| Untriaged | Open issues with no owner, label, plan, or PR |
| Quality risk | Failing CI, broken builds, flaky tests, blocked releases |

Check for blockers such as blocked labels, dependent issues, conflicting PRs,
stale plans, and recent changes that invalidate older plans.

## Ranking

Score each candidate with a compact, explainable rubric:

| Axis | Score |
| --- | --- |
| Unblocks other work | +3 |
| Already in flight | +3 |
| Fixes failed CI, build, or tests | +3 |
| Matches user focus | +2 |
| Resumes a partial plan | +2 |
| Addresses a recent bug or regression | +2 |
| Small enough for one focused session | +1 |
| Large multi-phase effort | -1 |
| Blocked | -5 |
| Already shipped or duplicate | -5 |

Recommend 3-5 candidates. Include at least one small useful win when available.
Never recommend work that appears already shipped.

## Output Shape

Use this structure:

```markdown
# Project Next Steps - <YYYY-MM-DD>

## Snapshot

- Branch: <name> (<clean/dirty>, <ahead/behind if known>)
- Open PRs: <count and short signal>
- Open issues: <count and label/theme signal>
- Active planning files: <count with pending or in-progress work>
- Recently shipped: <short summary>

## Flagged Concerns

- <dirty worktree, failing checks, stale PR, blocked plan, or "none">

## Recommended Next Steps

### 1. <Title> - <area> - score <N>

- **Why now**: <rationale tied to evidence>
- **Evidence**: <issue/PR/progress path/commit citation>
- **Blockers**: <none or blocker>
- **Suggested action**: <resume plan, fix directly, open plan, manage PR, triage issue>
- **Rough size**: XS/S/M/L

### 2. <Title> - <area> - score <N>

...

## Also Consider

- <lower priority candidate with evidence>
```

## Rules

- Every recommendation needs at least one verified citation: issue, PR,
  progress file path, commit SHA, or documentation path.
- Call out a dirty working tree before recommending new work.
- Prefer finishing in-flight work over starting something new.
- Keep the report short enough to scan in one screen when possible.
- After the report, ask which recommendation the user wants to pursue. Do not
  take hand-off actions without explicit approval.
