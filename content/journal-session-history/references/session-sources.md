# Session Sources

The helper script supports common local JSONL transcript layouts and keeps
parsing tolerant so schema changes do not break the workflow.

## Codex

Default root:

```text
${CODEX_HOME:-~/.codex}/sessions/YYYY/MM/DD/*.jsonl
```

Useful row types:

- `session_meta`: session id, timestamp, cwd, git metadata, model/provider.
- `turn_context`: cwd, timezone, model, sandbox policy.
- `event_msg`: user and assistant messages, command completion metadata.
- `response_item`: messages, tool calls, and patch payloads.

Parsing policy:

- Use dated folders in the inclusive date range for discovery.
- Extract visible user/assistant text.
- Extract command strings from shell tool calls.
- Extract changed paths from patch headers only.
- Skip developer/system instructions, reasoning internals, encrypted content,
  and full command output by default.

## Claude Code

Default root:

```text
~/.claude/projects/*/*.jsonl
```

Useful row types:

- `user`: visible user messages and tool-result messages.
- `assistant`: text blocks and tool-use blocks.
- `progress`: tool status and command output metadata.
- `file-history-snapshot`: file snapshots.

Parsing policy:

- Filter rows by timestamp converted to local date.
- Extract visible user/assistant text.
- Count tools from assistant `tool_use` blocks.
- Extract shell command strings and common write/edit paths.
- Skip raw command output and file snapshots by default.

## Hermes Agent

Default root:

```text
~/.hermes/sessions/
```

Two on-disk shapes share this directory:

- `session_<id>.json`: a full session record with `session_start`,
  `last_updated`, and a `messages` list. This is the complete, durable record.
- `<id>.jsonl`: a line-per-message log for recent sessions. Each row mirrors a
  `messages` entry.

The discovery step prefers the full `session_*.json` record and falls back to a
standalone `*.jsonl` only when no record exists for that session id, so a
session is never counted twice. The `sessions.json` index file is ignored.

Useful fields:

- `role`: `user`, `assistant`, or `tool`.
- `content`: visible message text.
- `tool_calls`: assistant tool invocations as `function.name` plus a JSON
  `function.arguments` string.

Parsing policy:

- Messages in full records carry no per-message timestamp, so the whole session
  is included when its `session_start`/`last_updated` window overlaps the
  requested range. JSONL rows are filtered by their own (coarse) timestamp, with
  the filename date as a fallback.
- Extract visible user/assistant text.
- Count tools from assistant `tool_calls` and shell commands from
  `terminal`-style `command`/`cmd` arguments.
- Collect file names from `path`/`file_path` arguments.
- Skip reasoning, encrypted content, tool result bodies, and the system prompt.

## Override Options

```bash
python3 content/journal-session-history/scripts/journal_history.py --codex-root /path/to/sessions
python3 content/journal-session-history/scripts/journal_history.py --claude-root /path/to/projects
python3 content/journal-session-history/scripts/journal_history.py --hermes-root /path/to/hermes/sessions
python3 content/journal-session-history/scripts/journal_history.py --source codex
python3 content/journal-session-history/scripts/journal_history.py --source claude
python3 content/journal-session-history/scripts/journal_history.py --source hermes
python3 content/journal-session-history/scripts/journal_history.py --project-filter my-project
```
