---
name: luna-subagent-delegation
description: Governs delegated work in Codex when the user requests subagents or an active runtime policy authorizes delegation. Routes bounded, low-risk, independently verifiable tasks to native Luna by default or to a preflighted external executor while the primary agent keeps decisions, integration, and final verification.
---

# Luna Subagent Delegation

This is the complete delegation runtime. Luna is the default executor; external executors are optional extensions configured by `external-agent-onboarding`.

## Preserve authority

This Skill never grants permission to delegate. Delegate only when the user or a higher-priority runtime instruction already authorizes subagents or external executors. The primary agent always owns intent, decomposition, product and architecture choices, permissions, integration, verification, and the final answer.

Keep work with the primary agent when it is simple, latency-sensitive, ambiguous, decision-heavy, destructive, security-sensitive, credential-bearing, an external write, or final release approval.

## Pass the delegation gate

Delegate only when every condition passes:

1. The subtask has one bounded goal, explicit scope, and objective completion criteria.
2. It can proceed without repeated product, architecture, permission, or user decisions.
3. Its result can be independently inspected or tested.
4. Parallelism or executor context is worth the coordination cost.
5. An eligible executor and runtime slot are actually available.

If any condition fails, execute directly. Do not delegate merely to save tokens.

## Route the task

Use native Luna for eligible code search, focused implementation, bounded research, test execution, log collection, static analysis, or mechanical refactoring. When the runtime supports model selection, request `gpt-5.6-luna` with `max` reasoning effort. If selection is unavailable, use the platform default and do not claim Luna ran.

Use an external executor only when all are true:

- an enabled local profile and real adapter exist;
- adapter preflight passes for the current workspace;
- capabilities and concrete allow/deny/approval rules cover the task; and
- its project context, environment access, or long-running capacity provides a meaningful advantage.

If external setup is missing, use `external-agent-onboarding`; it configures the extension but does not replace this routing policy.

## Control concurrency

- Check runtime capacity before spawning. Never claim a worker started until the spawn or adapter call succeeds.
- Parallel read-only tasks may share a workspace.
- Give each overlapping file to one writer. Use isolated worktrees for concurrent writers, or run them sequentially.
- Do not nest delegation when the runtime is at its agent limit. Preserve enough capacity for the primary agent to integrate results.

## Send one task contract

The following is this repository's implementation convention, not a native Codex wire protocol:

```yaml
contract_version: "1"
goal: one measurable outcome
workspace: absolute workspace path
allowed_scope: [files, directories, or systems]
allowed_actions: [read, modify_files, run_tests]
prohibited_actions: [external_write, destructive_action, credential_access]
acceptance_criteria: [observable completion conditions]
validation: [checks the worker must run]
required_report: executor-result-v1
```

Send only the context needed to execute that contract. Never ask a worker to expand its own permissions.

Require this result:

```yaml
status: completed | blocked | failed
summary: concise work performed
changed_artifacts: []
validation_results: []
risks: []
assumptions: []
unresolved: []
```

## Recover and verify

If spawning or invocation fails, either complete the bounded work directly when still authorized or report the concrete blocker. Never imply that a failed worker is active.

Treat every worker report as unverified. Inspect artifacts and evidence, rerun proportionate checks, resolve conflicts, and accept, revise, or discard the result. Report only verified outcomes.

## Label actual workers

Worker labels are optional UI labels, never real identities. Reuse a matching active entry from an existing `worker_roster`; otherwise use a transient `<role emoji> <given name>` label without modifying configuration just to persist it. Localize from the visible request language without inferring nationality, gender, or identity.

If the user retires a roster label, store only its retired status and at most one short, testable avoidance rule derived from a concrete shortcoming. Never reuse a retired label or keep biographies, ratings, histories, or performance narratives.

When at least one worker actually ran, include one short execution line listing only those workers, their executor, task, and terminal status. Omit it when no worker ran.
