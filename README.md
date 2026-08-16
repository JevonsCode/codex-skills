# Agent Skills

[中文](README.zh-CN.md)

Reusable agent skills for Codex-style and project-level AI workflows. This repository was originally named `codex-skills`; the working project name is **Agent Skills**.

## What is included

| Skill | Path | Purpose |
| --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | Turns product goals and design references into actionable frontend UI guidance. |
| User Taste | `skills/user-taste/SKILL.md` | Applies stated user preferences to underspecified design and engineering decisions. |
| Luna Subagent Delegation | `skills/luna-subagent-delegation/SKILL.md` | Complete delegation runtime: authorization gate, Luna-first routing, concurrency safety, task/result contracts, recovery, and primary-agent verification. |
| External Agent Onboarding | `skills/external-agent-onboarding/SKILL.md` | Optional add-on that registers and preflights Claude Code, local models, terminal agents, or custom agents for the Luna runtime. |

## Delegation architecture

`luna-subagent-delegation` is the complete core Skill and works by itself. It uses native Luna as the default eligible executor while the primary agent retains intent, architecture and permission decisions, integration, verification, and the final answer.

`external-agent-onboarding` depends on that core. It adds user-owned external executors but does not duplicate routing or handoff policy:

```text
primary agent → Luna delegation gate → native Luna (default)
                                   ↘ configured external executor (optional)
```

External execution is considered only when a stable profile, real adapter, workspace permission match, and preflight all pass. A bundled Claude Code adapter converts the shared task contract into a non-interactive structured invocation and normalizes the result; the primary agent still verifies the work.

## Custom configuration convention

The optional `~/.codex/executors.yaml`, Executor Task Contract, result schema, and adapter interface are conventions implemented by these Skills. They are not native Codex configuration or protocol.

Machine-specific adapter settings belong in local user-owned configuration. Never commit credentials, tokens, passwords, private command history, or personal shell pipelines. The shared profile uses concrete allow, deny, approval, and workspace boundaries; denied actions always win.

See:

- [Executor profile convention](skills/external-agent-onboarding/references/executor-profile.md)
- [Claude Code adapter](skills/external-agent-onboarding/references/claude-code-adapter.md)

## Install

Install the Luna core alone, or install both folders to enable onboarding:

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/luna-subagent-delegation" ~/.codex/skills/luna-subagent-delegation
ln -s "$PWD/skills/external-agent-onboarding" ~/.codex/skills/external-agent-onboarding
```

For project-level use, copy or link a Skill folder into `.codex/skills/` or `.agents/skills/`, according to the runtime. External Agent Onboarding must not be installed without Luna Subagent Delegation.

## Skill writing standard

Each `SKILL.md` should define activation conditions, decision rules, outputs, validation, and constraints. Keep shared Skills free of personal secrets, commands, and unsupported proprietary-system claims.

## Install with DingDongBuddy

[DingDongBuddy](https://github.com/JevonsCode/DingDongBuddy) manages Prompts, Skills, and MCP connections across supported agents. Import a Skill from its GitHub folder or `SKILL.md` URL:

- [Luna Subagent Delegation](https://github.com/JevonsCode/codex-skills/tree/main/skills/luna-subagent-delegation)
- [External Agent Onboarding](https://github.com/JevonsCode/codex-skills/tree/main/skills/external-agent-onboarding)

Enable Luna globally, dynamically, or for a specific project. Enable onboarding alongside it only where external executor setup is desired.
