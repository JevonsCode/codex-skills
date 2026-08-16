# Executor profile convention

Read this file when creating, editing, or validating `~/.codex/executors.yaml`.

This is a user-owned implementation convention for these Skills, not native Codex configuration. Paths and values below are placeholders; replace them only with facts confirmed from the user's machine.

## Schema

```yaml
version: 1
executors:
  - id: claude-code
    display_name: Claude Code
    type: terminal-agent
    enabled: false
    capabilities: [implementation, tests, debugging, review]
    priority: 50
    workspace_policy: explicit-projects
    workspaces:
      - /absolute/path/to/project
    allowed_actions: [read, modify_files, run_tests]
    approval_required_for: [external_write]
    denied_actions: [destructive_action, credential_access]
    adapter:
      id: claude-code-v1
      config_ref: ~/.codex/executor-adapters/claude-code.yaml
    result_contract_version: "1"
```

## Field rules

- `id`: unique, stable, lowercase local identifier. Renaming changes only `display_name`.
- `type`: `terminal-agent`, `local-model`, or `custom-agent`.
- `capabilities`: observed capabilities, not aspirations.
- `priority`: integer from 0 to 100; higher wins only after eligibility and safety checks tie. It never overrides permissions.
- `workspace_policy`: prefer `explicit-projects`. Use `inherit-current` only after the user confirms that boundary.
- `workspaces`: canonical absolute directories. Required for `explicit-projects`.
- `allowed_actions`: concrete actions the adapter may perform without another policy decision.
- `approval_required_for`: actions requiring task-specific user approval before handoff.
- `denied_actions`: unconditional denials; denial wins over approval and allowance.
- `adapter.config_ref`: local user-owned configuration reference. Do not embed tokens, passwords, raw shell pipelines, or private history.
- `result_contract_version`: must match the contract required by `luna-subagent-delegation`.

## Merge and validation rules

1. Read and parse the existing file before proposing changes.
2. Preserve unknown top-level keys and unknown keys on every executor.
3. Upsert exactly one executor by stable `id`; never append a duplicate.
4. Reject duplicate IDs, invalid priorities, missing explicit workspaces, nonexistent referenced workspaces, and overlapping allow/deny actions.
5. Show a redacted diff. Confirm before writing outside the active workspace.
6. Write to a sibling temporary file, parse and validate it, then atomically replace the target.

## Adapter contract

Preflight must report the resolved executable, version, workspace, permission mode, and whether a read-only smoke task passed. Runtime input and output must use the Executor Task Contract and `executor-result-v1` defined in `luna-subagent-delegation`.

Configuration is not proof of availability. Keep `enabled: false` until preflight succeeds; enable only after the user confirms the final diff.
