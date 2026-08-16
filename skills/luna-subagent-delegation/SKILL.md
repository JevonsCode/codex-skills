---
name: luna-subagent-delegation
description: Use this skill when working in Codex and a task contains bounded, low-risk, independently verifiable implementation, research, code-search, or test-execution work that may benefit from a Luna Max subagent. Keep planning, consequential decisions, integration, and final verification with the primary agent.
---

# Luna Subagent Delegation

## Purpose

Use Luna Max for well-scoped execution work while the current Codex agent remains responsible for the user's intent, task decomposition, safety boundaries, integration, and final answer.

## Decide whether to delegate

Delegate only when all of the following are true:

- The subtask has one clear goal and completion criteria.
- Its scope is independent enough that it can proceed without repeated product or architecture decisions.
- The primary agent can inspect and verify the returned result.
- The expected time or parallelism benefit exceeds the coordination cost.
- The work is low risk and does not require a user decision.

Good candidates include codebase search, focused implementation, test execution, log collection, static analysis, mechanical refactoring, and bounded research.

Do not delegate simple one-step work, ambiguous requests, architecture choices, security-sensitive decisions, external writes, destructive actions, credential access, or final release approval.

## Assign a worker identity

Before starting a delegated task, assign a concise fictional worker identity. Use it only as a task label; never imply that it identifies a real person.

Format the label as `<role emoji> <given name>`.

- Choose the emoji by task role: `🧑‍💻` for implementation, `🕵️` for investigation, `👮` for verification or QA, and `🧑‍🎨` for design work.
- Choose the name from the language or locale evident in the user's current request or stated preference. For example, use a Chinese-language name for a Chinese-language request, an English-language name for an English-language request, and a Spanish-language name for a Spanish-language request.
- Do not infer the user's real nationality, gender, or identity. If the language or locale is unclear, use a neutral international name.
- Give each concurrent worker a distinct label. Keep the label in the task request, terminal/session title where supported, and completion report.

At the end of the primary response, include one short execution summary listing only the active workers, their executor, and their assigned task. For example: `Execution: 🧑‍💻 林安 (Luna) — test failure triage; 👮 Alex (external agent) — full regression run.`

## Keep a lightweight worker roster

Use the optional `worker_roster` in `~/.codex/executors.yaml` for stable fictional worker labels.

- Match an active entry by executor, role, and locale. Reuse its label on later tasks.
- If no match exists, create one short label and persist only the executor, role, locale, label, and `active` status.
- If the user asks to retire a label because its work was unsatisfactory, ask one concise question about the concrete shortcoming. Summarize the answer into at most one short, testable `avoid` rule, then set the label's status to `retired`. Never assign or reuse retired labels; create a different label only when another worker is needed.
- Apply matching `avoid` rules to later tasks of the same executor and role. Keep no character biography, conversation history, ratings, or performance narrative. The label is a small UI detail, not a representation of a real employee.
- Omit the execution summary when no worker was delegated. Otherwise use at most one short line.

```yaml
worker_roster:
  - executor: luna
    role: implementation
    locale: zh
    label: "🧑‍💻 林安"
    status: active
    avoid: []
```

## Create the subtask

If the runtime supports selecting a subagent model, request `gpt-5.6-luna` with `max` reasoning effort. If it does not, use the platform's available subagent configuration without claiming that Luna Max was selected.

Give the subagent its worker identity and:

- the exact goal and relevant project context;
- allowed files, directories, and actions;
- constraints and prohibited actions;
- acceptance criteria and required validation;
- a request for a concise completion report.

Keep the task self-contained. Do not ask the subagent to make product, permission, or release decisions.

## Recover and verify

Treat the report as unverified. Inspect the changed files or produced evidence, run the relevant checks when proportionate, and decide whether to accept, revise, or discard the result.

Report only verified outcomes to the user. Preserve the primary agent's ownership of the final response and include the required short execution summary.
