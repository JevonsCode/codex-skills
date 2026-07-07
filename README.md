# Agent Skills

Reusable agent skills for Codex-style and project-level AI workflows.

This repository was originally named `codex-skills`; the working project name is now **Agent Skills**.

## Skills

| Skill | Path | Purpose |
| --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | Converts product goals, brand references, and page requirements into actionable frontend UI design guidance, component specs, design-token direction, interaction states, and implementation checklists. |
| Daily English Site | `skills/daily-english-site/SKILL.md` | Generates and maintains a JSON-driven Daily English learning website for GitHub Pages, including review quizzes, daily word schema, mobile UI rules, privacy-safe metadata, and publishing steps. |

## Recommended structure

```text
skills/
  <skill-name>/
    SKILL.md
```

Use each skill by copying or symlinking its folder into the agent runtime skill directory, for example:

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/frontend-ui-design" ~/.codex/skills/frontend-ui-design
```

For project-level usage, copy a skill folder into a project-local skills directory such as `.codex/skills/` or `.agents/skills/`, depending on the agent runtime convention used by the project.

## Skill writing standard

Each `SKILL.md` should be practical and executable:

1. Define when the skill should be used.
2. Convert vague user intent into concrete outputs.
3. Include decision rules, not only style descriptions.
4. Specify expected deliverables, review checklist, and implementation constraints.
5. Avoid copying protected brand assets or pretending to reproduce another company's proprietary design system.

## Current focus

The skills focus on converting reusable product, design, learning, and delivery workflows into executable instructions that agents can apply consistently.
