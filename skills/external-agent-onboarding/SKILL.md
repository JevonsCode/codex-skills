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

After the user confirms the answers, create or update a user-local configuration using this schema:

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

Keep startup details in a separate local adapter or user-owned configuration file. Do not place machine-specific shell commands in this shared Skill or a repository-visible profile.

## Routing guidance

Select an external agent only when it has a relevant capability or meaningful existing context that outweighs the handoff cost.

Typical use:

- Use a configured terminal agent for a longer-running test suite, environment-specific debugging, or a project where it already has useful context.
- Use a lower-cost Codex subagent for short, self-contained, parallelizable work.
- Keep requirements, architecture, permission decisions, integration, and final verification with the primary Codex agent.

## Safe handoff

Before handoff, send a structured task containing the goal, workspace, scope, constraints, acceptance criteria, and required report.

Require the external agent to return:

- status: completed, blocked, or failed;
- summary of work performed;
- changed artifacts or files;
- validation results;
- risks, assumptions, and unresolved issues.

Treat returned content as unverified until the primary agent checks it. Require explicit user approval for external writes, destructive actions, credential access, or actions outside the configured workspace.
