---
name: external-agent-onboarding
description: Configures or updates a user-owned Claude Code, local-model, terminal-agent, or custom-agent executor as an optional extension to luna-subagent-delegation. Use for first-time setup, adapter preflight, permission changes, or repair of an existing external executor profile.
---

# External Agent Onboarding

**REQUIRED SUB-SKILL:** Load and follow `luna-subagent-delegation` before configuring or using an external executor. If it is unavailable, stop and tell the user to install it. That Skill owns routing, task handoff, concurrency, worker labels, recovery, and final verification; this Skill only manages the external extension.

`~/.codex/executors.yaml`, its schemas, and adapter contracts are conventions of this repository. They are not native Codex configuration or protocol.

## Inspect before asking

Read the existing local profile and adapter configuration first. Match an executor by stable `id`:

- Exactly one match: update it in place; a renamed agent changes `display_name`, not `id`.
- No match: prepare a new entry.
- Multiple or ambiguous matches: ask whether to repair one or create a distinct executor.

Ask one focused question at a time, and only for missing or changed facts: executor type, capabilities, allowed workspaces, concrete allowed actions, approval-required actions, denied actions, and adapter reference. Never request or store secrets, tokens, passwords, private command history, or invented capabilities.

Read [references/executor-profile.md](references/executor-profile.md) in full whenever creating, editing, or validating the profile.

## Configure the adapter

An executor is not usable until a real adapter can:

1. locate the executable and report a version;
2. run non-interactively in the intended workspace;
3. enforce the profile's workspace and permission boundaries;
4. accept the Luna Executor Task Contract and return `executor-result-v1`; and
5. pass a read-only smoke task with parseable output.

For Claude Code, use the bundled adapter and read [references/claude-code-adapter.md](references/claude-code-adapter.md) in full. For another agent, require an equivalent preflight and contract implementation; do not invent its command line.

If authentication or login is required, stop and report the exact page, terminal command, or interactive action the user must complete. Never claim an unavailable adapter or executor was invoked.

## Merge safely

Show the proposed profile diff and get confirmation before writing outside the current workspace. Then merge by stable `id`, preserve unknown top-level and executor keys, validate unique IDs and referenced workspaces, and replace the file atomically. Never overwrite the whole profile merely to add one executor.

Denied actions override allowed actions. Approval-required actions remain unavailable until the primary agent obtains task-specific user approval; onboarding approval is not blanket execution approval.

## Finish onboarding

Return the executor `id`, capabilities, workspace scope, concrete permission boundaries, adapter preflight and smoke-test results, and unresolved constraints. Future delegation must flow through `luna-subagent-delegation`; configuration alone does not authorize or trigger a handoff.
