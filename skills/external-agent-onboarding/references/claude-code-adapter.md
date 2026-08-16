# Claude Code adapter

Read this file when registering, validating, or repairing a Claude Code executor.

The bundled `scripts/claude_code_adapter.py` is a reusable adapter, not a personal command. It invokes Claude Code without a shell, refuses `bypassPermissions`, sends the Luna task contract over stdin rather than exposing it in the process arguments, requests JSON Schema output, and emits a normalized result.

## Preflight

Run the non-billing binary and workspace check first:

```bash
python3 scripts/claude_code_adapter.py preflight \
  --workspace /absolute/path/to/project \
  --claude-bin claude
```

Preflight also checks that non-interactive print mode, structured output, JSON Schema, permission mode, and tool allowlists are supported, and reports whether `--bare` is available. Record the resolved binary and version in the user-owned adapter configuration. Do not store credentials.

A safe local starting point is:

```yaml
version: 1
adapter_id: claude-code-v1
binary: /resolved/path/from/preflight
permission_mode: dontAsk
bare: false
timeout_seconds: 1800
allowed_tools_by_action:
  read: [Read, Glob, Grep]
  modify_files: [Edit, Write]
  run_tests: []
```

The binary path is a machine-specific placeholder until preflight resolves it. Keep command-capable entries such as `Bash(...)` empty until the user confirms a project-specific rule and the read-only smoke test passes. The primary agent converts only the current task's allowed actions into repeated `--allowed-tool` arguments.

## Read-only smoke task

Create a temporary JSON task using the exact contract from `luna-subagent-delegation`, limited to one harmless file and `allowed_actions: [read]`. Then run:

```bash
python3 scripts/claude_code_adapter.py run \
  --task-file /absolute/path/to/read-only-task.json \
  --claude-bin claude \
  --permission-mode dontAsk \
  --allowed-tool Read
```

`dontAsk` denies tools that are neither read-only nor explicitly allowed. Add tools only when both the executor profile and the current task contract allow them. Use `acceptEdits` only for a confirmed `modify_files` task. The adapter intentionally provides no `bypassPermissions` mode.

The adapter also rejects `Edit`, `Write`, or `NotebookEdit` unless the task allows `modify_files`, rejects `acceptEdits` for read-only tasks, and rejects `Bash` unless the task allows tests or commands.

By default Claude Code loads the user's and project's normal configuration, which can include hooks, MCP servers, and project instructions. Use only confirmed workspaces and inspect that configuration during onboarding. Add `--bare` only when the user deliberately wants an isolated scripted run and has configured `ANTHROPIC_API_KEY` or the selected provider credentials required by bare mode; an interactive Claude Code subscription login is not used there.

## Result handling

- Exit code `0`: the adapter returned a valid normalized result; `status` may still be `blocked` or `failed`.
- Exit code `2`: adapter, process, authentication, timeout, or schema failure. Read the JSON result and surface any `requires_user_action` exactly.
- Never treat stdout outside the normalized JSON object as verified work.

The primary agent must still inspect artifacts and rerun proportionate validation under `luna-subagent-delegation`.
