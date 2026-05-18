# laloloops-skill — Agent Context

## Shared Rules

These rules are inherited from the parent workspace and **must** be followed in every interaction.

### Git Author Identity

All commits use the project identity. Always use the local git author:

```
Lalo Loops <laloloops@proton.me>
```

### No AI Co-authorship

- Never add `Co-Authored-By` trailers for any AI tool.
- Never reference AI tools in commit messages.

### Human-sounding Commits

Imperative mood subject line, optional body explaining why. Write like a developer, not a bot.

### GitHub CLI

Use `ghl` (not bare `gh`) for all GitHub CLI operations scoped to the LaloLoops account.

### Privacy

Never commit PII, personal references, credentials, API keys, or anything that could de-anonymize the person behind Lalo Loops. Audit every file before committing.

### Brand Voice

Read `../laloloops-branding/brand/voice_guide.md` before making design or copy changes. Respect the visual palette (orange `#E8872B`, cream `#FDF0DC`, black `#1A1A1A`) and tone.

### Repository Settings

- Do not force push unless explicitly asked.
- Repository lives under `https://github.com/LaloLoops/`.
- This repository is **public** — audit every file before committing for PII or secrets.

---

## Project

TBD — fill in once scope is decided.
