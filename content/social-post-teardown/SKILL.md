---
name: social-post-teardown
description: Break down a social post into its big idea, sentence structure, word choice, engagement drivers, and psychological tactics, then turn the pattern into a step-by-step replication template the user can apply to their own ideas. Use when the user pastes a tweet, LinkedIn post, thread, Instagram caption, TikTok hook, Reddit post, or any short-form social copy and asks why it works or how to imitate it.
---

# Social Post Teardown

Dissect a single short-form social post and return both an analysis and a
reusable template. This skill answers "why does this post work, and how do I
write one like it?" It is read-only and analytical. Do not invent metrics,
author intent, or engagement numbers that the user did not provide.

Use this skill when the user:

- Pastes a social post and asks for a teardown, breakdown, or analysis.
- Wants to understand structure, voice, hooks, rhythm, or psychology of a post.
- Wants a step-by-step recipe to replicate the style with their own topic.

Do not use this skill for:

- Generating new posts from scratch with no reference post.
- Multi-post content strategy, calendars, or channel planning.
- Long-form blog or essay critique.

## Inputs

Infer inputs from the request. Ask only if the post itself is missing.

| Parameter | Meaning |
| --- | --- |
| `post` | Required. The full text of the social post being analyzed. |
| `platform` | Optional. `twitter`, `linkedin`, `instagram`, `tiktok`, `threads`, `reddit`, or similar. Shapes assumptions about format and norms. |
| `context` | Optional. Author, audience, niche, or reported engagement numbers. Use only as user-provided context, not as assumed fact. |
| `replicate_topic` | Optional. The user's own idea to express in the same style. If provided, produce a worked example. |
| `voice` | Optional. The user's tone or brand constraints to respect in the replication example. |
| `depth` | `standard` by default. `quick` returns sections 1-4 and the template only. `deep` includes line-by-line annotation. |

If the post is not pasted, ask for it before doing anything else. Do not guess
at a post from memory.

## Method

Work through the post in this order. Keep each pass tight and evidence-led.

1. **Read the whole post twice.** First for meaning, second for mechanics.
2. **Identify the big idea.** One sentence. What is the post actually arguing,
   promising, revealing, or making the reader feel?
3. **Map the structure.** Mark the hook, the body beats, the turn or twist,
   and the payoff or CTA. Note sentence count, average length, and any
   deliberate rhythm (short-short-long, list, one-liner, etc.).
4. **Inspect word choice.** Note vocabulary tier (plain, technical, slangy,
   biblical, corporate), repeated words, concrete nouns vs. abstractions,
   sensory detail, contrast pairs, and any signature phrase.
5. **Locate engagement drivers.** What makes a reader stop, react, save, or
   reply? Tie each driver to a specific line.
6. **Name the psychological tactics.** Use the taxonomy in
   `references/psychological-tactics.md`. For each tactic, quote the exact
   span in the post that triggers it.
7. **Extract the pattern.** Convert the post into a reusable skeleton with
   slot names the user can refill.
8. **Replicate (if `replicate_topic` is provided).** Produce one worked
   example in the user's voice constraints. Otherwise show how to fill the
   skeleton in general terms.

If any pass produces nothing meaningful, say so plainly. A short post may have
no real "structure" beyond the hook, and that itself is the lesson.

## Evidence Rules

- Quote the post when claiming a tactic, hook, or word choice is doing work.
  Use short inline quotes, not paragraph dumps.
- Do not assert that the post "went viral", "got X likes", or "performed well"
  unless the user supplied that fact in `context`. Otherwise describe the
  craft, not the outcome.
- Do not psychoanalyze the author. Talk about what the text does to readers,
  not what the author secretly intended.
- If a tactic could be read multiple ways, name the most defensible reading
  and flag the ambiguity in one line.

## Output Structure

Use this structure for `depth=standard`:

```markdown
# Social Post Teardown

Platform: <platform or "unspecified">
Post length: <N sentences / N words>

## 1. The Post

> <verbatim post, preserved line breaks>

## 2. Big Idea

<one-sentence thesis of the post>

## 3. Structure

- **Hook**: "<quoted opener>" - <what it does>
- **Body beats**: <ordered list of beats with one-line purpose each>
- **Turn / payoff**: "<quoted line>" - <why this is the punch>
- **CTA or close**: <explicit, implicit, or none>
- **Rhythm**: <sentence length pattern, line breaks, list use>

## 4. Word Choice

- **Vocabulary tier**: <plain / technical / slangy / etc.>
- **Repeated or anchor words**: <list with counts if useful>
- **Concrete vs. abstract**: <ratio observation with examples>
- **Signature moves**: <contrast pairs, sensory detail, numbers, naming, etc.>

## 5. Why People Engage

- <driver 1> - tied to "<quoted span>"
- <driver 2> - tied to "<quoted span>"
- <driver 3> - tied to "<quoted span>"

## 6. Psychological Tactics

| Tactic | Where it appears | What it does |
| --- | --- | --- |
| <name from taxonomy> | "<quoted span>" | <effect on reader> |

## 7. Replication Template

```
<skeleton with {{slot}} placeholders that mirror the original structure>
```

**How to fill it:**

1. <step describing how to choose the hook slot>
2. <step describing how to choose the body beats>
3. <step describing how to choose the turn or payoff>
4. <step describing how to choose the close or CTA>
5. <step describing voice and rhythm constraints to preserve>

## 8. Worked Example

<Only include if `replicate_topic` was provided. Apply the skeleton to that
topic in the user's voice. Keep it the same approximate length as the original.>
```

For `depth=quick`, output sections 1-4 and section 7 only.

For `depth=deep`, add a final section:

```markdown
## 9. Line-By-Line Notes

| Line | Quote | What it is doing |
| --- | --- | --- |
| 1 | "<line>" | <function> |
```

## Voice Rules

- Default voice for the teardown itself is neutral, plain, and craft-focused.
  Write like a copy editor explaining a trick, not a guru selling a course.
- Do not use emoji, hashtags, or hype words in the teardown unless the post
  itself uses them and you are quoting.
- When producing the worked example in section 8, match the original post's
  voice and rhythm, then apply any user `voice` constraints on top.
- Avoid claims like "this is the best hook ever" or "guaranteed to go viral".
  Describe mechanics, not promises.

## Final Checks

Before returning:

- Every tactic and driver is tied to a quoted span from the post.
- The replication template can be filled in without re-reading the analysis.
- No invented metrics, author quotes, or backstory.
- If `replicate_topic` was provided, section 8 exists and is the same shape
  as the original post.
- If the post was too short or too thin to support a full teardown, the output
  says so and trims sections rather than padding them.

## Bundled Resources

- `references/psychological-tactics.md`: short, neutral taxonomy of common
  persuasion and engagement tactics used in short-form social copy, with
  one-line definitions and example trigger phrases.
