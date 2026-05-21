---
name: agent-comm
description: Coordinate two or more agent sessions through a shared file mailbox, compact state file, status log, and explicit human approval gate. Use when one agent coordinates or builds while another verifies, monitors, deploys, submits, or operates a live/risky environment from the same filesystem.
---

# Agent Comm

Use a tiny shared file protocol when separate agent sessions need durable,
inspectable coordination. The goal is not an agent framework. The goal is clear
ownership, a per-handoff phase contract, and a hard gate before irreversible
actions.

Use this skill when:

- Two agent sessions can read and write the same workspace.
- One session coordinates while another executes, verifies, observes, or owns a
  live environment.
- The work has custom phases or instructions that should be visible to both
  sessions.
- A human must explicitly approve an irreversible step.

Do not use this pattern when one agent can safely complete the work directly, or
when the agents do not share a reliable filesystem.

## File Protocol

Create a repository-local communication directory unless the user asks for a
different location:

```text
.agent-comm/
├── inbox.md
├── status.md
└── state.json
```

Keep one writer per file:

| File | Writer | Reader | Purpose |
| --- | --- | --- | --- |
| `.agent-comm/inbox.md` | Coordinator | Executor | Instructions, command list, constraints, current ask |
| `.agent-comm/status.md` | Executor | Coordinator | Progress, command results, blockers, standby state |
| `.agent-comm/state.json` | Coordinator | Executor | Machine-readable phase and approval gate |

If an executor must update `state.json`, state that exception explicitly in
`inbox.md`. Otherwise the executor treats `state.json` as read-only.

## State Model

Keep state tiny and valid JSON. Do not hardcode a universal phase list in the
skill. The coordinator defines the phase names, allowed actions, standby rules,
and terminal phases for each handoff in `inbox.md`.

`state.json` only records the current switch position:

```json
{
  "phase": "<current-phase>",
  "approved": false,
  "approved_action": null,
  "poll_interval_seconds": 20,
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_by": "coordinator"
}
```

When approving an irreversible action, update only the fields needed for the
handoff:

```json
{
  "phase": "<approved-phase>",
  "approved": true,
  "approved_action": "<approved-action>",
  "poll_interval_seconds": 20,
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_by": "coordinator"
}
```

When the handoff is finished or stopped, close the gate:

```json
{
  "phase": "<terminal-phase>",
  "approved": false,
  "approved_action": null,
  "poll_interval_seconds": 20,
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_by": "coordinator"
}
```

The executor may run an irreversible action only when all required conditions
match the inbox:

- `phase` matches the approved phase named in the phase contract.
- `approved` is `true`.
- `approved_action` matches the action named in `inbox.md`.
- The human approval required by the coordinator has already been recorded.

If the state file is missing, malformed, contradictory, or stale in a risky way,
the executor must enter the safe behavior defined in `inbox.md`. It must not
infer approval from chat history, command names, or partial state.

## Coordinator Workflow

1. Identify the workspace, coordinator, executor, phases, allowed actions,
   approval phrase, standby behavior, and stop conditions.
2. Create `.agent-comm/` and initialize `state.json` with `approved: false`.
3. Write `inbox.md` with the phase contract and exact executor instructions.
4. Create `status.md` with an initial waiting or not-started entry.
5. Start or prompt the executor session.
6. Monitor `status.md`, `state.json`, and any live notes or logs.
7. Do not set the approved phase until the human explicitly approves the risky
   action in the current coordination context.
8. After the executor reports completion, set a terminal phase and
   `approved: false`.

## Executor Workflow

1. Read `inbox.md` and `state.json` before starting.
2. Write a timestamped status entry before running commands.
3. Run only actions allowed by the current phase.
4. Reread `state.json` before every major step and immediately before any
   irreversible action.
5. When the inbox-defined standby point is reached, write results to
   `status.md`, then enter standby.
6. While in standby, poll `state.json` at `poll_interval_seconds`.
7. Run the irreversible action exactly once only when the approval conditions
   match.
8. Report final result to `status.md`.
9. If the phase is terminal or unknown, follow the safe behavior defined in
   `inbox.md`.

Never write secrets, tokens, cookies, `.env` values, credential fingerprints, or
private account details into `inbox.md`, `status.md`, live notes, or chat. When
reporting command output, summarize sensitive sections instead of copying them.

## Inbox Template

````markdown
# Executor Inbox

## Role

You are the executor for this handoff. The coordinator owns instructions and
state. You own status reporting and command execution.

## Workspace

`<absolute-or-relative-workspace-path>`

## Required Reads

Before each major step, reread:

- `.agent-comm/inbox.md`
- `.agent-comm/state.json`

## Required Writes

Write progress, command results, blockers, and standby state to:

- `.agent-comm/status.md`

## Redaction Rules

Do not expose secrets, tokens, `.env` values, private account details, or other
sensitive identifiers in notes or chat.

## Phase Contract

Use only the phases defined here. For each phase, follow the allowed actions and
safe behavior.

| Phase | Allowed actions | Standby? | Terminal? |
| --- | --- | --- | --- |
| `<phase-name>` | `<commands or behavior>` | `<yes/no>` | `<yes/no>` |

Unknown phase behavior: `<stop, standby, or ask coordinator>`

## Commands

Run these while `state.json` phase is `<phase-name>`:

```sh
<command 1>
<command 2>
```

After `<standby condition>`, stop before `<approved action>` and enter standby.

## Standby

While standing by, reread `.agent-comm/state.json` every
`poll_interval_seconds`. Continue waiting while `approved` is false.

Only run `<irreversible command>` once if state says:

```json
{
  "phase": "<approved-phase>",
  "approved": true,
  "approved_action": "<approved action>"
}
```

If phase is terminal or unknown, do not run the irreversible command.
````

## Status Template

```markdown
# Executor Status

## Current State

- Time: `<timestamp>`
- Phase observed: `<phase>`
- Status: `<not started | running | standby | blocked | done>`
- Next action: `<next command or waiting condition>`

## Results

| Time | Step | Result | Notes |
| --- | --- | --- | --- |
| `<timestamp>` | `<command or action>` | `<pass/fail/skipped>` | `<short notes>` |

## Blockers

- `<none or concrete blocker>`
```

## Executor Prompt Template

When the executor is a separate session, give it a prompt like this:

```text
Use the shared file handoff protocol.

Workspace:
<workspace path>

Read before each major step:
- .agent-comm/inbox.md
- .agent-comm/state.json

Write progress and results to:
- .agent-comm/status.md

Follow the redaction rules in inbox.md. Do not expose secrets, tokens, .env
values, credentials, private account details, or sensitive identifiers.

Run only the commands allowed by the phase contract in inbox.md. When the
inbox-defined standby condition is reached, enter standby and poll state.json at
the configured interval.

Only run the irreversible action once if state.json phase matches the approved
phase in inbox.md, approved is true, and approved_action matches the action
named in inbox.md. If phase is terminal or unknown, do not run the irreversible
action.
```

## Operating Rules

- Prefer append-only status entries. If rewriting the summary at the top, keep
  the detailed result table intact.
- Make the approval phrase explicit to the human, but do not store private
  human identity details in repository files.
- Keep verbose live notes separate from compact state. If a live-notes skill is
  available and the user wants visibility, ask the executor to maintain notes
  outside the repository.
- For observer or backup sessions, give them read-only instructions and require
  promotion in `inbox.md` before they execute live commands.
- If the coordinator loses confidence in the handoff, set the configured safe
  terminal phase and `approved: false` before investigating.

## Completion Criteria

The handoff is complete only when:

- `status.md` records the final executor result.
- `state.json` is set to a terminal phase with `approved: false`.
- The coordinator has summarized final outcome, verification, and any residual
  risk to the user.
