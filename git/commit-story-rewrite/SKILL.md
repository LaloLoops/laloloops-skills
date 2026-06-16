---
name: commit-story-rewrite
description: Rewrites an existing Git branch into a clean, reviewer-friendly commit story and semantic commit stack while preserving the final tree. Use when the user asks to reorganize, squash, split, reorder, or rewrite current branch history into semantic commits, commit stacking, a coherent review story, integrate fix commits into the original commits they fix, create a local backup branch before rewriting, or force-push a rewritten branch after explicit approval. Do not use for ordinary one-off commits, JJ-only commit stacking, or deploying code.
---

# Commit Story Rewrite

Rewrite a Git branch into a semantic commit stack that reads as a coherent review story.
The final branch must be net-equivalent to the original intended branch state,
but no commit should introduce code that a later commit merely fixes.

Use Git. If the repository explicitly requires JJ for this task, switch to the
repo's JJ workflow instead.

## Invariants

- Create a local backup branch before rewriting.
- Preserve unrelated dirty work; never fold it into the rewritten branch by accident.
- The rewritten tip tree matches the original intended tip tree.
- Each commit is a semantic layer: one reviewable concern, not one file bucket.
- Each commit is definitive at that point in the story: no WIP, fixup, "address review", or "fix tests" commits remain.
- Earlier commits do not depend on later commits.
- Tests, migrations, fixtures, generated clients, and docs live with the behavior they validate or explain unless the repo has a stronger convention.
- Force-push only when the user explicitly asks for it.

## Preflight

Read repo instructions first, especially Git identity, GitHub wrapper, and branch
rules. Then collect evidence before changing history:

```bash
git status --short --branch
git branch --show-current
git remote -v
git fetch --all --prune
git log --oneline --decorate --graph --date=short --all -n 40
git merge-base HEAD origin/main
```

If the worktree has unrelated unstaged or untracked changes, preserve them before
rewriting. Prefer leaving them untouched when possible; if a rewrite operation
would mix them into the index, stash them with a descriptive message and restore
them after verification.

## Backup

Make a local branch at the current tip. Do not check it out or push it unless
asked.

```bash
branch="$(git branch --show-current)"
stamp="$(date +%Y%m%d-%H%M%S)"
backup="backup/${branch}/${stamp}"
git branch "$backup" HEAD
```

Record the base and original tip:

```bash
base="$(git merge-base HEAD origin/main)"
original="$backup"
git diff --stat "$base..$original"
git diff --name-status "$base..$original"
```

Use the backup for recovery and net-equivalence checks.

## Plan The Story

Inspect the current commits and final diff:

```bash
git log --oneline --decorate --reverse "$base..HEAD"
git diff --stat "$base..HEAD"
git diff "$base..HEAD" -- <path>...
```

Design a linear sequence that a reviewer can follow:

- foundation/schema/config before code that consumes it
- shared libraries and generated clients before service integration
- backend/API changes before frontend usage when the frontend depends on them
- UI state and behavior before polish only when polish is independently reviewable
- tests with the code they prove
- mechanical moves/renames isolated only when they are large enough to obscure behavior

Integrate fixes directly into the layer they correct. If validation finds a bug in
commit 2 while you are already at commit 5, amend commit 2 and replay the later
commits; do not add a "fix commit" unless the user explicitly wants audit-trail
commits.

For published branches, state the rewrite impact before pushing: old commit SHAs
will be replaced, and reviewers may need to refresh.

## Rewrite

For a full branch rewrite, the most reliable path is usually to rebuild the stack
from the merge base while preserving the working tree:

```bash
git reset --soft "$base"
git reset
```

Then create commits in the planned order. Stage deliberately:

```bash
git add <paths>
git add -p <paths>
git diff --cached --stat
git diff --cached
git commit -m "<imperative subject>"
```

When a commit needs a fix after it exists, prefer fixup plus autosquash:

```bash
git add <paths>
git commit --fixup=<target-sha>
GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash "$base"
```

Use concise, human commit messages. Subjects should be imperative and specific.
Bodies are optional; add one when it explains why the layer exists, not what the
diff already says. Do not add AI/tool attribution or co-authored trailers unless
the repo explicitly requires them.

## Validate

Check the rewritten branch before any push:

```bash
git log --oneline --decorate --reverse "$base..HEAD"
git range-diff "$base..$original" "$base..HEAD"
git diff --exit-code "$original" HEAD
git diff --check "$base..HEAD"
```

`git diff --exit-code "$original" HEAD` must be empty unless the user asked to
change the final tree during the rewrite. If it is not empty, stop and explain the
intentional difference or repair the rewrite.

Run the narrowest meaningful validation for the changed code. For high-risk
rewrites, validate each commit or use:

```bash
git rebase --exec '<test command>' "$base"
```

After validation, restore any unrelated stashed work and confirm it remains
uncommitted.

## Push

Only push after explicit user approval. Always fetch first and use lease
protection:

```bash
git fetch origin
git status --short --branch
git push --force-with-lease origin HEAD:<remote-branch>
```

If the remote changed unexpectedly since the backup or since the last fetch, stop
and inspect before pushing.

## Report

Report:

- backup branch name
- base branch and merge base
- final commit order with one-line purpose for each commit
- net-equivalence result against the backup
- validation run and outcome
- whether a force push happened, and to which remote branch
- any dirty unrelated work preserved
