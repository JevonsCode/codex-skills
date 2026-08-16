# Agent Skills

[中文](README.zh-CN.md)

Reusable agent skills for Codex-style and project-level AI workflows.

This repository was originally named `codex-skills`; the working project name is now **Agent Skills**.

## What is included

| Skill | Path | Purpose |
| --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | Turns product goals, design references, and page requirements into actionable frontend UI guidance. |
| User Taste | `skills/user-taste/SKILL.md` | Applies a user's stated preferences and decision style to UI, architecture, product, code, writing, and design tradeoffs. |
| Luna Subagent Delegation | `skills/luna-subagent-delegation/SKILL.md` | Delegates bounded, low-risk, independently verifiable work to a Luna Max subagent while the primary agent retains planning and final verification. |
| External Agent Onboarding | `skills/external-agent-onboarding/SKILL.md` | Guides users through configuring Claude Code, local models, and other external agents for delegated development, testing, and verification. |

## Delegation workflow

The two delegation Skills can be installed together:

1. **Luna Subagent Delegation** handles short, self-contained work that benefits from parallel execution.
2. **External Agent Onboarding** registers terminal agents such as Claude Code and routes longer development, full test suites, deep debugging, or complex verification to eligible external executors.

The primary Codex agent always retains user-intent interpretation, architecture and permission decisions, integration, and final verification.

## External agent configuration

The onboarding Skill creates a local executor profile at `~/.codex/executors.yaml`. The profile records capabilities, risk limits, allowed actions, and approval boundaries. Keep machine-specific commands, credentials, and secrets out of this repository.

To conserve Codex usage without wasting external-agent capacity:

- Prefer external agents for lengthy independent development, full test suites, deep debugging, and complex verification.
- Keep small or latency-sensitive work, ambiguous requirements, consequential decisions, and final acceptance with Codex.

## Worker labels and feedback

Delegated workers can use a lightweight fictional label such as `🧑‍💻 林安` or `👮 Alex`. Labels are localized from the user's stated or visible language preference, not inferred identity.

A local roster reuses labels for the same executor, role, and locale. If a user retires a label after poor work, the Skill asks for one concrete shortcoming, stores one concise avoidance rule, and does not reuse that label. This feature stores no character biographies, conversation histories, or performance narratives.

## Install

Copy or symlink a Skill folder into the agent runtime's Skill directory:

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/luna-subagent-delegation" ~/.codex/skills/luna-subagent-delegation
```

For project-level use, copy a Skill folder into a project-local directory such as `.codex/skills/` or `.agents/skills/`, according to the agent runtime.

## Skill writing standard

Each `SKILL.md` should:

1. Define when the Skill should be used.
2. Convert vague intent into concrete outputs.
3. Include decision rules, not only descriptions.
4. Specify deliverables, validation, and constraints.
5. Avoid protected brand assets and proprietary system claims.


## Install with DingDongBuddy

[DingDongBuddy](https://github.com/JevonsCode/DingDongBuddy) is a local companion for managing Prompts, Skills, and MCP connections across supported Agents. Use its Skill import flow to install a Skill directly from a GitHub folder URL or a `SKILL.md` URL.

Import these Skills:

- [Luna Subagent Delegation](https://github.com/JevonsCode/codex-skills/tree/main/skills/luna-subagent-delegation)
- [External Agent Onboarding](https://github.com/JevonsCode/codex-skills/tree/main/skills/external-agent-onboarding)

After import, choose whether to enable the Skill globally, dynamically, or for a specific project. Keep machine-specific commands and credentials in local configuration, not in the shared Skill.
