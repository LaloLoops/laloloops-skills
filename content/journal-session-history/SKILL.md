---
name: journal-session-history
description: Summarize development work from local agent session transcripts. Use when the user asks what happened today or on a specific date, wants to recover prior agent work, or needs source material from local session history before writing a journal entry.
---

# Journal Session History

Create a concise journal-oriented summary from local agent session history.
This skill answers "what happened in prior sessions?" If the user wants writing
based on the current conversation instead, use `journal-session-current`.

This skill is read-only. It inspects local transcript files and reports what it
finds.

## Quick Start

Default to today's local date unless the user gives a date.

```bash
python3 content/journal-session-history/scripts/journal_history.py --date YYYY-MM-DD --source all
```

Use inclusive ranges when the user asks for multiple days:

```bash
python3 content/journal-session-history/scripts/journal_history.py --date-from YYYY-MM-DD --date-to YYYY-MM-DD --source all
python3 content/journal-session-history/scripts/journal_history.py --date-from YYYY-MM-DD --source all
```

If output is large, narrow it:

```bash
python3 content/journal-session-history/scripts/journal_history.py --source codex --max-items 40
python3 content/journal-session-history/scripts/journal_history.py --source claude --project-filter my-project
```

Use `--format json` when a structured intermediate is easier to analyze. Raw
transcript excerpts are omitted by default. Add `--include-excerpts` only for
local-only review when the user explicitly wants source snippets.

## Workflow

1. Determine the target date or inclusive date range. Convert relative dates to
   `YYYY-MM-DD`.
2. Run the bundled `journal_history.py` script. Do not inspect raw transcript
   files directly unless the digest is insufficient.
3. Read `references/session-sources.md` only if source discovery or transcript
   schema behavior matters.
4. Use the script output as evidence. Keep every claim grounded in transcript-derived
   items.
5. Mark uncertain facts as uncertain or omit them.

## Content Rules

- Start with what was actually worked on: project area, task, obstacle,
  decision, implementation, verification, and result.
- Prefer concrete evidence over broad claims: tools, files, commands,
  decisions, checks, and handoffs.
- Keep raw transcript output short. Summarize instead of pasting long logs or
  messages.
- Do not include raw transcript excerpts unless the user explicitly asks for
  them.
- If there is not enough material, say so and report the source/date range that
  was checked.

## Suggested Output Shape

```markdown
# Journal Session History

Date: <YYYY-MM-DD or range>
Sources: <Codex/Claude counts>

## Executive Summary

- <2-4 bullets about workstreams and shareable themes>

## Story Briefs

### Story 1: <title>

- Task: <what had to be done>
- Challenge: <what made it non-trivial>
- How it was solved: <method, implementation, workflow>
- Result: <what changed or became clear>
- Lesson: <public-safe lesson>
- Content idea: <journal or content angle worth developing later>

## Draft Content Starters

<Optional ideas that can be passed to `journal-session-current`>
```

## Bundled Resources

- `scripts/journal_history.py`: scans local Codex and Claude JSONL sessions for
  a date range and emits Markdown or JSON.
- `references/session-sources.md`: default transcript locations and schema
  notes.
