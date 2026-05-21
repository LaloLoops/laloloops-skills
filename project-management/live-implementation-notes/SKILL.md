---
name: live-implementation-notes
description: Maintain a live timestamped implementation-notes HTML file outside the repository while doing coding or product implementation work. Use when the user asks to track an ongoing implementation, keep running implementation notes, or expose decisions, tradeoffs, changes, and verification in real time.
---

# Live Implementation Notes

Keep a user-readable implementation notes HTML document current while work is
happening. The document is a concise implementation journal, not a final report:
update it at meaningful checkpoints so the user can inspect progress without
interrupting the agent.

Use `assets/implementation-notes.template.html` as the default format. Preserve
the template structure, section IDs, CSS, and visual hierarchy unless the user
asks for a different format.

## Workflow

1. Before implementation work starts, create a unique notes file outside the
   repository, normally in the operating system's temporary directory.
2. Copy this skill's `assets/implementation-notes.template.html` into that
   unique path.
3. Immediately tell the user the exact created file path in a short progress
   update so they can open it.
4. Before making substantive edits, fill in the task, scope, assumptions, and
   first "Current focus" entry.
5. During the work, update the file whenever any of these happen:
   - A decision is made that was not explicit in the request.
   - A file or module behavior changes in a user-visible or architecturally
     relevant way.
   - A tradeoff, risk, blocker, or assumption appears.
   - A verification command is run, skipped, blocked, or fails.
   - The current focus changes.
6. Before the final response, make one last update with final status, completed
   work, verification results, residual risks, and handoff notes.
7. In the final response, mention the notes file path and summarize only the
   highest-signal items.

## File Naming

Store generated notes outside the repository unless the user explicitly asks for
a repository path. Use this filename shape:

```text
<temp-dir>/implementation-notes-YYYYMMDD-HHMMSS-shortid.html
```

Generate the timestamp from local time. Use a short unique suffix, such as six
lowercase hex characters, to avoid collisions.

Portable Python sequence:

```python
from datetime import datetime
from pathlib import Path
import shutil
import tempfile
import uuid

template = Path("project-management/live-implementation-notes/assets/implementation-notes.template.html")
notes_file = Path(tempfile.gettempdir()) / f"implementation-notes-{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}.html"
shutil.copyfile(template, notes_file)
print(notes_file)
```

After creating the file, immediately send a progress update in this form:

```text
Created live implementation notes: <temp-dir>/implementation-notes-YYYYMMDD-HHMMSS-shortid.html
```

## HTML Format Rules

- Keep the document self-contained: inline CSS, no remote assets, no JavaScript,
  no build step.
- Preserve these section IDs: `overview`, `status`, `decisions`, `changes`,
  `tradeoffs`, `verification`, `handoff`.
- Keep the top summary scannable. Put detailed chronology in the logs below.
- Use short factual entries with timestamps. Local time is fine; include the
  date when work spans more than one day.
- Use status pills consistently: `Planned`, `Doing`, `Done`, `Blocked`,
  `Changed`, `Risk`, `Verified`, `Skipped`.
- Keep newest "Current focus" at the top, but keep log entries chronological
  inside each section unless the file already uses reverse chronology.
- Record decisions and reasons, not hidden reasoning traces.
- Do not create or update notes files in the repository unless the user
  explicitly requests a repository path.
- If the user already has an implementation notes file, preserve useful
  existing entries and migrate only if needed to match this format.

## Entry Guidance

Write notes that answer what a user would ask if they paused the agent:

- What is being worked on right now?
- What changed since the last checkpoint?
- What decisions were made because the request did not specify them?
- What tradeoffs or risks remain?
- What has been verified, and what could not be verified?
- What should the next agent or human know before continuing?

Prefer concrete file/module names and command names. Avoid vague progress
entries like "working on implementation" unless paired with the specific area
being changed.

## Completion Criteria

The skill has been applied only if a unique implementation-notes HTML file
exists, the agent announced its path immediately after creation, the file uses
the predefined HTML format, and it has been updated at least once near the
beginning and once at the end of the implementation.
