---
name: agent-session-launcher
description: Launch Claude Code or Codex in a chosen repository, usually inside tmux, after asking a short pre-launch checklist for agent, session mode, permission posture, workspace, and task prompt. Use when the user wants an external coding agent session started and attachable later.
---

# Agent Session Launcher

Start an external coding agent session in a predictable, attachable way. The
main use case is launching Claude Code or Codex inside a repository so the user
can come back later, attach to tmux, and continue from a live session instead of
starting cold.

The skill is opinionated about one thing: **do not launch until the user has
confirmed the launch profile**. Ask a short checklist first, then start the
session, verify it is actually running, and report the attach command.

## When to Use

Use this skill when the request sounds like:

- "Open Claude Code in this repo and let it work on this prompt."
- "Start Codex on this task so I can come back later."
- "Launch an interactive coding agent session in tmux."
- "Run an external agent in this folder with a specific prompt."
- "Start the agent now, verify it is running, and tell me how to attach."

Do not use this skill when:

- the work should stay inside the current agent session,
- a simple shell command is enough,
- a durable scheduled job is the better fit,
- the user has not yet identified the target repository or folder.

## Pre-Launch Checklist

Before launching, ask the user for the following unless they already specified
all of it clearly.

### 1. Agent choice

Ask which agent to launch:

- Claude Code
- Codex CLI

### 2. Session mode

Ask whether the session should be:

- **Interactive in tmux**
- **Inline / one-shot command**

Interpretation:

- **Interactive in tmux** = long-lived, attachable, good for iterative work,
  exploration, and tasks that may need follow-up.
- **Inline / one-shot command** = bounded execution that exits when done, good
  for focused analysis, reviews, and artifact generation.

### 3. Permission / autonomy posture

Ask how much autonomy the launched agent should have:

- **Safe / normal permissions**
- **More automatic / fewer interruptions**
- **Skip permissions / maximum autonomy**

Never silently choose the most dangerous option. If the user wants it, make the
trade-off explicit before launch.

Suggested mapping:

#### Claude Code

- Safe / normal → `claude`
- More automatic → `claude --permission-mode auto` when suitable
- Skip permissions → `claude --dangerously-skip-permissions`

#### Codex CLI

- Safe / normal → default approvals plus chosen sandbox
- More automatic → choose an approval policy such as `-a on-request` or `-a never`
- Skip permissions → `--dangerously-bypass-approvals-and-sandbox`

### 4. Workspace and prompt

Confirm:

- repository or folder path
- exact prompt/task to run
- whether the agent should write an output artifact to a file
- any branch/worktree assumptions that matter before launch

### 5. Terminal policy

If using interactive tmux, do **not** ask which terminal app to use unless the
user explicitly requests a GUI terminal. tmux is the boundary. Launching the
session and giving the attach command is sufficient.

## Default Recommendation

If the user asks for a default recommendation, prefer:

- **Claude Code** for exploratory coding and analysis
- **Interactive in tmux** when the task is open-ended or likely to need follow-up
- **Inline / one-shot** when the task is bounded and should finish on its own
- **Normal permissions** unless the user explicitly wants more autonomy
- **tmux only** unless the user explicitly asks to open a GUI terminal window

## Launch Procedure

### 1. Verify prerequisites

Before launching, verify the basics:

- the target path exists,
- the repository/worktree is the intended one,
- the relevant binary exists,
- tmux exists for interactive mode,
- authentication is ready when it can be checked quickly.

Typical checks:

```sh
which claude && claude --version
which codex && codex --version
which tmux && tmux -V
git rev-parse --show-toplevel && git branch --show-current
```

If multiple worktrees or checkouts exist, identify the correct one before
launching.

### 2. Use a prompt file for long prompts

If the task prompt is non-trivial, write it to a temporary file and load/paste
from there instead of trying to cram a huge shell-escaped string into the launch
command.

### 3. Interactive Claude Code in tmux

Preferred pattern:

```sh
SESSION='name'
REPO='/path/to/repo'
tmux kill-session -t "$SESSION" 2>/dev/null || true
tmux new-session -d -s "$SESSION" -x 160 -y 50 -c "$REPO" 'claude'
sleep 5
```

Then:

- accept the trust dialog if it appears,
- paste or load the prompt,
- submit it,
- monitor with `tmux capture-pane`.

If the user explicitly requested skip-permissions:

```sh
claude --dangerously-skip-permissions
```

For bounded non-interactive Claude work:

```sh
claude -p "..." --max-turns 10
```

### 4. Interactive Codex in tmux

Preferred pattern:

```sh
SESSION='name'
REPO='/path/to/repo'
tmux kill-session -t "$SESSION" 2>/dev/null || true
tmux new-session -d -s "$SESSION" -x 160 -y 50 -c "$REPO" 'codex'
sleep 5
```

Useful flags:

- inline mode: `codex exec "..."`
- inline but same terminal scrollback: `codex --no-alt-screen`
- sandbox choice: `-s read-only|workspace-write|danger-full-access`
- approval choice: `-a untrusted|on-request|never`
- skip everything only with explicit consent:
  `--dangerously-bypass-approvals-and-sandbox`

### 5. Optional GUI terminal opening

Only do this if the user explicitly asks for it.

The reliable core is tmux. GUI terminal automation is secondary and should not
block the actual launch.

If requested, try to open a terminal app and run:

```sh
tmux attach -t <session>
```

If GUI automation is flaky, still proceed with the tmux launch and report the
attach command.

### 6. Verify the launch

Before reporting success, verify the session by inspection:

```sh
tmux ls
tmux capture-pane -t <session> -p -S -80
```

Confirm one of these is visible:

- the agent banner,
- active tool work,
- a waiting prompt,
- completed one-shot output.

## What to Report Back

Report at least:

- agent used,
- mode used,
- repository path,
- branch or worktree if relevant,
- tmux session name,
- current status: running, waiting, or completed,
- attach command,
- output artifact path if one was requested.

Suggested concise response shape:

- Agent: Claude Code / Codex
- Mode: interactive tmux / inline
- Repo: `...`
- Branch: `...`
- Session: `...`
- Status: running / waiting / completed
- Attach: `tmux attach -t ...`
- Notes: normal permissions / more automatic / skip-permissions, plus any retry or GUI note

## Common Pitfalls

1. **Launching before asking the checklist.**
   If the user did not clearly specify agent, mode, and permission posture, ask.

2. **Treating GUI terminal opening as the primary task.**
   The real task is launching the agent session. tmux comes first.

3. **Using the wrong repository or worktree.**
   Verify the actual checkout before launch.

4. **Trying to shell-quote a huge prompt inline.**
   Use a prompt file.

5. **Claiming success without inspecting the pane.**
   Always verify with `tmux capture-pane` or equivalent.

6. **Silently escalating permissions.**
   Dangerous autonomy modes require explicit user consent.

7. **Forgetting the attach command.**
   The launch is incomplete if the user does not know how to reattach.

## Verification Checklist

- [ ] Agent choice confirmed
- [ ] Session mode confirmed
- [ ] Permission/autonomy level confirmed
- [ ] Repository/workdir verified
- [ ] Binary availability checked
- [ ] tmux availability checked for interactive mode
- [ ] Session launched
- [ ] Running state verified from output
- [ ] Attach command reported
- [ ] Any optional GUI-terminal attempt reported separately from the real launch
