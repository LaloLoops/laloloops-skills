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

## Override Options

```bash
python3 skills/content/journal-session-history/scripts/journal_history.py --codex-root /path/to/sessions
python3 skills/content/journal-session-history/scripts/journal_history.py --claude-root /path/to/projects
python3 skills/content/journal-session-history/scripts/journal_history.py --source codex
python3 skills/content/journal-session-history/scripts/journal_history.py --source claude
python3 skills/content/journal-session-history/scripts/journal_history.py --project-filter my-project
```
