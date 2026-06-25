# Agent Skills Repository Guide

This repository stores reusable agent skills.

## Project name

Use **Agent Skills** as the project name in documentation and references.

The historical GitHub repository slug may remain `codex-skills` unless the repository itself is renamed in GitHub settings.

## Repository structure

```text
skills/
  <skill-name>/
    SKILL.md
skills/manifest.json
README.md
```

## Adding or editing a skill

1. Create or update `skills/<skill-name>/SKILL.md`.
2. Keep the skill practical: include when to use it, decision rules, output format, implementation notes, and a checklist.
3. Update `skills/manifest.json` when adding a new skill.
4. Do not copy proprietary brand assets, logos, or exact protected design systems.
5. Prefer Chinese writing when the skill is primarily used by Chinese-speaking product/frontend teams.

## Current skill

- `frontend-ui-design`: frontend UI design skill based on reusable principles from Notion, Google, Figma, and Airbnb.