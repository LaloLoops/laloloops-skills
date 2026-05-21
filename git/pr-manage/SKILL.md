---
name: pr-manage
description: Manage a pull request lifecycle from the current branch through creation, review, CI fixes, and merge. Use when the user asks to open a PR, request review, address review feedback, fix failing checks, monitor status, or merge once review and checks are ready.
---

# PR Manage

Own a pull request lifecycle until it is merged or blocked by credentials,
permissions, conflicts, repository policy, or an explicit user stop.

This skill may create commits, push branches, create or update PRs, request
review, address feedback, fix checks, and merge when ready. Stop before any
write action if the worktree contains unrelated changes or the repository's
publishing policy is unclear.

## CLI Selection

Use the repository's configured GitHub command. Default to `gh`, but respect
local wrappers or environment configuration when present.

Recommended command variable:

```bash
GH_CMD="${GH_CMD:-gh}"
```

If the repository instructions require a wrapper, use that wrapper instead of
bare `gh`. Do not encode account-specific rules in this skill; those belong in
local agent instructions.

## Operating Rules

- Inspect `git status -sb` and relevant diffs before staging or committing.
- Do not stage unrelated local changes.
- Treat review comments as suggestions. Apply feedback that improves
  correctness, maintainability, tests, security, or clarity.
- Decline harmful, stale, already-satisfied, or out-of-scope feedback with a
  concise PR comment.
- Do not treat green CI as review approval. Wait for an explicit review signal
  when review was requested.
- Keep polling until the PR is merged or a stop condition is reached.

## Bootstrap

Verify repository and host access:

```bash
git status -sb
git branch --show-current
git remote get-url origin
"${GH_CMD:-gh}" auth status
"${GH_CMD:-gh}" repo view --json nameWithOwner,defaultBranchRef,autoMergeAllowed,deleteBranchOnMerge,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
```

Resolve or create the PR for the current branch:

```bash
"${GH_CMD:-gh}" pr view --json number,url,state,isDraft,headRefName,baseRefName
```

If no PR exists, push the branch with tracking if needed, then create the PR
against the repository default branch unless the user specified another base.
Prefer a ready-for-review PR unless the user explicitly asks for a draft.

After the PR exists and is not draft, request review when requested using the
repository's normal mechanism. Examples:

```bash
"${GH_CMD:-gh}" pr edit <pr> --add-reviewer <reviewer>
"${GH_CMD:-gh}" pr comment <pr> --body "$REVIEW_REQUEST_BODY"
```

Use `REVIEW_REQUEST_BODY` only when the repository documents a bot or comment
trigger. Only repeat a review request after new commits, after actionable
feedback has been addressed or declined, or after a CI fix changed code.

## Poll Loop

Poll every 60-180 seconds unless repository policy suggests otherwise. Each
cycle must inspect review/comments and checks.

```bash
"${GH_CMD:-gh}" pr view <pr> --json number,url,state,isDraft,mergeable,mergeStateStatus,reviewDecision,headRefOid,headRefName,baseRefName,comments,reviews,statusCheckRollup
"${GH_CMD:-gh}" pr checks <pr> --json name,state,bucket,link,workflow,completedAt
```

For thumbs-up reactions on the PR body:

```bash
"${GH_CMD:-gh}" api -H "Accept: application/vnd.github+json" \
  "/repos/<owner>/<repo>/issues/<number>/reactions" \
  --jq '.[] | select(.content == "+1") | {user:.user.login, created_at}'
```

For inline review state, use a GitHub review-thread helper if one is available.
Otherwise inspect pull request `reviewThreads` with GraphQL, including
resolution state, outdated state, file path, line, author, body, and URL.

## Review Completion Gate

After requesting review, do not merge until the latest request has a terminal
review signal for the current `headRefOid`.

Terminal signals:

- A valid `+1` thumbs-up reaction on the PR body from a reviewer account.
- A formal approving review.
- Review comments or review body feedback for the current head commit, with
  every actionable item addressed or explicitly declined with rationale.

Non-terminal signals:

- No comments yet.
- Only an `eyes` reaction.
- Green CI with no review result.
- Review data from before the latest review request.
- Review data for an older commit.

## Feedback Handling

When feedback appears:

1. Cluster feedback by file or behavior area.
2. Separate actionable comments from approvals, duplicates, stale comments, and
   informational notes.
3. Implement necessary changes locally.
4. Run targeted verification.
5. Commit and push the fixes.
6. Re-request review if code changed.

If feedback will not be addressed, post a concise rationale on the PR or thread.

## CI Handling

The PR is not ready while any required or visible check is queued, running,
pending, failing, cancelled, or timed out.

If a check fails:

1. Inspect the failing check URL or logs.
2. Identify the root cause before editing.
3. Rerun once only if the failure is clearly flaky and the repo allows it.
4. If code changes are needed, make the smallest fix, run local verification,
   commit, push, and re-request review.

Useful commands:

```bash
"${GH_CMD:-gh}" pr checks <pr> --json name,state,bucket,link,workflow,completedAt
"${GH_CMD:-gh}" run view <run-id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha
"${GH_CMD:-gh}" run view <run-id> --log
```

## Merge Gate

Merge only when:

- The PR is open and not draft.
- No actionable review comments remain unresolved.
- The latest review request has a terminal review signal for the current head.
- Required checks are finished and successful.
- The PR is mergeable and branch protection is satisfied.

Determine allowed merge methods:

```bash
"${GH_CMD:-gh}" repo view --json autoMergeAllowed,deleteBranchOnMerge,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
```

Prefer the repository's established merge convention. If no convention is
visible, use the first allowed method in this order: squash, merge commit,
rebase.

```bash
"${GH_CMD:-gh}" pr merge <pr> --delete-branch --squash
"${GH_CMD:-gh}" pr merge <pr> --delete-branch --merge
"${GH_CMD:-gh}" pr merge <pr> --delete-branch --rebase
```

If the PR is otherwise ready but required checks are still pending and the
repository allows auto-merge, enable auto-merge with the selected method.

## Stop Conditions

Stop and report clearly when:

- The PR is merged.
- Authentication or permissions block required actions.
- Branch protection or merge policy cannot be inferred.
- Merge conflicts or unrelated dirty state require user direction.
- Review feedback conflicts with the requested work or repo policy.
- The user asks to stop.

Final report should include PR URL, merge status or blocker, checks consulted,
review signal used, and any follow-up required.
