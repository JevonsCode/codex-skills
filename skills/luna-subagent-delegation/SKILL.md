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

## Create the subtask

If the runtime supports selecting a subagent model, request `gpt-5.6-luna` with `max` reasoning effort. If it does not, use the platform's available subagent configuration without claiming that Luna Max was selected.

Give the subagent:

- the exact goal and relevant project context;
- allowed files, directories, and actions;
- constraints and prohibited actions;
- acceptance criteria and required validation;
- a request for a concise completion report.

Keep the task self-contained. Do not ask the subagent to make product, permission, or release decisions.

## Recover and verify

Treat the report as unverified. Inspect the changed files or produced evidence, run the relevant checks when proportionate, and decide whether to accept, revise, or discard the result.

Report only verified outcomes to the user. Preserve the primary agent's ownership of the final response.
