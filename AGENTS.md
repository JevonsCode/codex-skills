# Agent Skills Repository Guide

This repository stores reusable agent skills under the project name **Agent Skills**. The historical GitHub slug may remain `codex-skills`.

## Repository structure

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml       # optional UI metadata
    references/              # optional on-demand guidance
    scripts/                 # optional deterministic utilities and tests
skills/manifest.json
README.md
README.zh-CN.md
```

## Editing a Skill

1. Define when it activates, its decision rules, required output, validation, and constraints.
2. Keep `SKILL.md` concise; move conditional detail into one-level references.
3. Add deterministic scripts only when they close a real reliability gap, and test them.
4. Update `skills/manifest.json` and both READMEs when public behavior changes.
5. Keep personal commands, secrets, credentials, and machine-specific state out of the repository.
6. Do not copy proprietary brand assets or claim native support for a custom convention.

## Delegation architecture

- `luna-subagent-delegation` is the complete delegation runtime and native-Luna default.
- `external-agent-onboarding` is an optional extension that depends on the Luna Skill and only configures external profiles and adapters.
- `~/.codex/executors.yaml` and the executor contracts are repository conventions, not native Codex protocol.
- Routing, concurrency, worker labeling, recovery, and final verification belong only to the Luna Skill; do not duplicate them in onboarding.

## Current Skills

- `frontend-ui-design`
- `user-taste`
- `luna-subagent-delegation`
- `external-agent-onboarding`
