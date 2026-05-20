---
name: journal-session-current
description: Generate a generic development journal entry and content ideas from the current conversation. Use when the user wants a factual journal summary, lessons learned, open threads, or reusable content ideas from work that just happened.
---

# Journal Session Current

Create a structured journal entry and content ideas from the current
conversation. This skill answers "how should we write about this session?" Use
`journal-session-history` first when the source material lives in older local
agent transcripts.

This is a read-only content skill. The current conversation is the primary
source by default. If the user provides a digest, use that digest as the source
of truth. Do not invent drama, metrics, reactions, results, or lessons.

## Relationship To Session History

- `journal-session-history`: summarizes work from local agent session history.
- `journal-session-current`: turns the current conversation or provided notes
  into a journal entry and reusable content ideas.

When both are useful, run the history skill first, then use its output as notes
for this skill.

## Modes

Infer the mode from the user's request:

| Mode | Use When | Output |
| --- | --- | --- |
| `journal` | The user wants a factual record. | Journal summary only. |
| `quick` | The user wants the short version. | Summary plus 2-3 content ideas. |
| `ideas` | The user wants angles to develop later. | Summary plus expanded idea list. |
| custom hint | The user names a topic or audience. | Bias the ideas toward that hint. |

Use neutral framing unless the user explicitly asks for a specific voice.

## Evidence Extraction

Scan the current conversation or provided notes for:

- Work completed: features, fixes, docs, assets, decisions, or plans.
- Why it mattered: user problem, workflow improvement, quality improvement, or
  learning.
- How it happened: tools, commands, iterations, checks, failures, handoffs, and
  constraints.
- Verification: tests, screenshots, review, lint, manual checks, or "not run".
- Open threads: unfinished work, risks, next steps, and follow-up questions.
- Reusable ideas: techniques, tradeoffs, debugging patterns, collaboration
  patterns, or future content angles.

If a claim cannot be supported by the conversation or notes, omit it or mark it
as uncertain.

## Voice Rules

Default voice is neutral, practical, and evidence-led:

- Write like a practitioner documenting real work.
- Start with concrete session details, then generalize.
- Prefer short sentences and plain nouns.
- Keep implementation details when they make the lesson clearer.
- Use first person only when natural and supported by the source.
- Do not use emoji, hashtags, or platform gimmicks unless requested.
- Avoid corporate SaaS filler and AI hype.

Do not include a fixed author biography, workplace context, style stance, or
audience assumption. If the user provides a style or audience guide, follow it
for that task only.

## Output Structure

Use this structure unless the user asks for a narrower output:

```markdown
# Journal Session Current

Date: <YYYY-MM-DD>
Source: <conversation | session history | provided notes>
Session focus: <one-line factual summary>

## 1. Journal Summary

- <3-6 factual bullets about what happened>

**Key decisions:**

- <decision and rationale, if any>

**Open threads:**

- <unfinished work, risk, or follow-up, if any>

## 2. Content Ideas

1. <Idea title> - <what it would cover and why it is useful>
2. <Idea title> - <what it would cover and why it is useful>
3. <Idea title> - <what it would cover and why it is useful>

## 3. Reusable Notes

- <phrasing, examples, commands, lessons, or caveats worth preserving>

## 4. Follow-Up Questions

- <questions to answer before turning ideas into finished content>

```

For `journal`, output only section 1. For `quick`, keep sections 1-2 short and
omit sections 3-4 unless requested.

## Final Checks

Before returning:

- Every claim is grounded in the conversation or user-provided notes.
- The content can stand without extra context.
- Any missing verification is stated plainly.
