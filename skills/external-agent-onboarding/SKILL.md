---
name: external-agent-onboarding
description: Use this skill when a Codex user wants to configure their own Claude Code, local model, terminal agent, or other external agent for delegated development, testing, or verification work. Guide a first-use configuration interview, produce a local executor profile, and define safe routing boundaries without embedding personal commands or secrets in the shared skill.
---

# External Agent Onboarding

## Purpose

Set up a user's local external agents so Codex can later choose them for bounded development, test, and verification work.

This Skill configures policy and routing metadata. It does not assume that a named agent is installed, accessible, or safe to invoke.

## First-use interview

When no executor profile exists, ask one focused question at a time. Collect:

1. Which external agents the user wants to register.
2. Each agent's display name and supported capabilities, such as implementation, tests, debugging, review, or research.
3. Whether it has useful existing project context or requires a terminal workspace.
4. Which workspaces it may access.
5. The highest permitted risk level: low, medium, or high.
6. Whether it may modify files, run tests, access credentials, or perform external writes.
7. How it is started and how its result is returned to Codex.

Never request or store API keys, passwords, tokens, or private command history. Do not invent a command, capability, or permission.

## Produce a local profile

After the user confirms the answers, create or update `~/.codex/executors.yaml` using this schema. Read this file first on later uses; ask only for missing or changed information:

```yaml
version: 1
executors:
  - id: unique-local-id
    type: terminal-agent | local-model | custom-agent
    enabled: true
    capabilities: [implementation, tests]
    priority: 50
    max_risk: low | medium | high
    workspace_policy: explicit-projects | inherit-current
    allowed_actions: [read, modify_files, run_tests]
    approval_required_for: [external_write, destructive_action, credential_access]
    result_contract: structured-report
```

Keep startup details in a separate local adapter or user-owned configuration file. Do not place machine-specific shell commands in this shared Skill or a repository-visible profile. If an adapter is unavailable, do not claim that the external agent was invoked.

## Routing guidance

Select an external agent only when it has a relevant capability or meaningful existing context that outweighs the handoff cost. Prefer an eligible external agent for lengthy independent development, full test suites, deep debugging, or complex verification when the goal is to conserve Codex usage. Keep small, latency-sensitive, or decision-heavy work with Codex.

Typical use:

- Use a configured terminal agent for a longer-running test suite, environment-specific debugging, or a project where it already has useful context.
- Use a lower-cost Codex subagent for short, self-contained, parallelizable work.
- Keep requirements, architecture, permission decisions, integration, and final verification with the primary Codex agent.

## Assign a worker identity

Before starting a delegated task, assign a concise fictional worker identity. Use it only as a task label; never imply that it identifies a real person.

Format the label as `<role emoji> <given name>`.

- Choose the emoji by task role: `🧑‍💻` for implementation, `🕵️` for investigation, `👮` for verification or QA, and `🧑‍🎨` for design work.
- Choose the name from the language or locale evident in the user's current request or stated preference. For example, use a Chinese-language name for a Chinese-language request, an English-language name for an English-language request, and a Spanish-language name for a Spanish-language request.
- Do not infer the user's real nationality, gender, or identity. If the language or locale is unclear, use a neutral international name.
- Give each concurrent worker a distinct label. Keep the label in the task request, terminal/session title where supported, and completion report.

At the end of the primary response, include one short execution summary listing only the active workers, their executor, and their assigned task. For example: `Execution: 🧑‍💻 林安 (Luna) — test failure triage; 👮 Alex (external agent) — full regression run.`

## Safe handoff

Before handoff, send the worker identity and a structured task containing the goal, workspace, scope, constraints, acceptance criteria, and required report.

Require the external agent to return:

- status: completed, blocked, or failed;
- summary of work performed;
- changed artifacts or files;
- validation results;
- risks, assumptions, and unresolved issues.

Treat returned content as unverified until the primary agent checks it. Require explicit user approval for external writes, destructive actions, credential access, or actions outside the configured workspace. Include the required short execution summary in the primary response.
