#!/usr/bin/env python3
"""Run one Executor Task Contract through Claude Code and normalize its result."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional


SAFE_PERMISSION_MODES = {"dontAsk", "acceptEdits", "plan"}
REQUIRED_CLI_OPTIONS = (
    "--print",
    "--output-format",
    "--json-schema",
    "--permission-mode",
    "--allowedTools",
)
# A local version lookup should be immediate; this bound prevents a broken launcher hanging onboarding.
VERSION_CHECK_TIMEOUT_SECONDS = 15
# External test and implementation tasks can be long, but must not wait forever by default.
DEFAULT_RUN_TIMEOUT_SECONDS = 1800
# Keep process diagnostics useful without dumping an arbitrarily large or sensitive transcript.
ERROR_DETAIL_LIMIT = 2000
TASK_LIST_FIELDS = {
    "allowed_scope",
    "allowed_actions",
    "prohibited_actions",
    "acceptance_criteria",
    "validation",
}
NONEMPTY_TASK_LIST_FIELDS = {
    "allowed_scope",
    "allowed_actions",
    "acceptance_criteria",
    "validation",
}
TASK_REQUIRED_FIELDS = {
    "contract_version",
    "goal",
    "workspace",
    "required_report",
} | TASK_LIST_FIELDS
RESULT_LIST_FIELDS = {
    "changed_artifacts",
    "validation_results",
    "risks",
    "assumptions",
    "unresolved",
}
RESULT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["completed", "blocked", "failed"]},
        "summary": {"type": "string"},
        "changed_artifacts": {"type": "array", "items": {"type": "string"}},
        "validation_results": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "unresolved": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "status",
        "summary",
        "changed_artifacts",
        "validation_results",
        "risks",
        "assumptions",
        "unresolved",
    ],
}


class AdapterError(RuntimeError):
    """Raised when the adapter cannot safely run or normalize an executor."""


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_task(task: Any) -> Dict[str, Any]:
    if not isinstance(task, dict):
        raise AdapterError("task contract must be a JSON object")

    missing = sorted(TASK_REQUIRED_FIELDS - set(task))
    if missing:
        raise AdapterError("task contract is missing: " + ", ".join(missing))

    if task["contract_version"] != "1":
        raise AdapterError("contract_version must be \"1\"")
    if not _nonempty_string(task["goal"]):
        raise AdapterError("goal must be a non-empty string")
    if task["required_report"] != "executor-result-v1":
        raise AdapterError("required_report must be \"executor-result-v1\"")

    for field in sorted(TASK_LIST_FIELDS):
        value = task[field]
        if not isinstance(value, list) or not all(_nonempty_string(item) for item in value):
            raise AdapterError(f"{field} must be an array of non-empty strings")
        if field in NONEMPTY_TASK_LIST_FIELDS and not value:
            raise AdapterError(f"{field} must contain at least one entry")

    overlap = sorted(set(task["allowed_actions"]) & set(task["prohibited_actions"]))
    if overlap:
        raise AdapterError("actions cannot be both allowed and prohibited: " + ", ".join(overlap))

    workspace_input = Path(str(task["workspace"])).expanduser()
    if not workspace_input.is_absolute():
        raise AdapterError("workspace must be an absolute path")
    workspace = workspace_input.resolve()
    if not workspace.is_dir():
        raise AdapterError(f"workspace is not an existing directory: {workspace}")

    normalized = dict(task)
    normalized["workspace"] = str(workspace)
    return normalized


def validate_execution_policy(
    task: Dict[str, Any], permission_mode: str, allowed_tools: List[str]
) -> None:
    actions = set(task["allowed_actions"])
    tool_names = {tool.split("(", 1)[0] for tool in allowed_tools}
    write_tools = {"Edit", "Write", "NotebookEdit"}

    if permission_mode == "acceptEdits" and "modify_files" not in actions:
        raise AdapterError("acceptEdits requires modify_files in allowed_actions")
    if tool_names & write_tools and "modify_files" not in actions:
        raise AdapterError("Edit and Write tools require modify_files in allowed_actions")
    if "Bash" in tool_names and "run_tests" not in actions and "run_commands" not in actions:
        raise AdapterError("Bash requires run_tests or run_commands in allowed_actions")


def resolve_binary(binary: str) -> str:
    expanded = os.path.expanduser(binary)
    has_path_separator = os.sep in expanded or (os.altsep and os.altsep in expanded)
    candidate = Path(expanded).resolve() if has_path_separator else None
    resolved = str(candidate) if candidate and candidate.is_file() else shutil.which(expanded)
    if not resolved or not os.access(resolved, os.X_OK):
        raise AdapterError(f"Claude Code executable was not found or is not executable: {binary}")
    return resolved


def preflight(binary: str, workspace: str) -> Dict[str, Any]:
    resolved_workspace = Path(workspace).expanduser().resolve()
    if not resolved_workspace.is_dir():
        raise AdapterError(f"workspace is not an existing directory: {resolved_workspace}")
    resolved_binary = resolve_binary(binary)
    try:
        process = subprocess.run(
            [resolved_binary, "--version"],
            cwd=str(resolved_workspace),
            check=False,
            capture_output=True,
            text=True,
            timeout=VERSION_CHECK_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise AdapterError(
            f"Claude Code version check timed out after {VERSION_CHECK_TIMEOUT_SECONDS} seconds"
        ) from exc
    if process.returncode != 0:
        detail = (process.stderr or process.stdout or "unknown error").strip()[:ERROR_DETAIL_LIMIT]
        raise AdapterError(f"Claude Code version check failed: {detail}")
    version = (process.stdout or process.stderr).strip()
    if not version:
        raise AdapterError("Claude Code version check returned no version")

    try:
        help_process = subprocess.run(
            [resolved_binary, "--help"],
            cwd=str(resolved_workspace),
            check=False,
            capture_output=True,
            text=True,
            timeout=VERSION_CHECK_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise AdapterError(
            f"Claude Code option check timed out after {VERSION_CHECK_TIMEOUT_SECONDS} seconds"
        ) from exc
    if help_process.returncode != 0:
        detail = (help_process.stderr or help_process.stdout or "unknown error").strip()
        raise AdapterError(f"Claude Code option check failed: {detail[:ERROR_DETAIL_LIMIT]}")
    help_text = "\n".join([help_process.stdout, help_process.stderr])
    missing_options = [option for option in REQUIRED_CLI_OPTIONS if option not in help_text]
    if missing_options:
        raise AdapterError(
            "Claude Code CLI is missing required options: " + ", ".join(missing_options)
        )
    return {
        "ok": True,
        "binary": resolved_binary,
        "version": version.splitlines()[0],
        "workspace": str(resolved_workspace),
        "required_options": "supported",
        "supports_bare": "--bare" in help_text,
    }


def build_prompt() -> str:
    return (
        "Read the JSON task contract from stdin and execute it. Stay inside its workspace, scope, "
        "allowed actions, and acceptance criteria. Do not expand permissions or ask the user "
        "to approve a prohibited action. If the contract cannot be completed safely, return "
        "status blocked and explain the unresolved constraint. Return only the requested "
        "structured result."
    )


def build_command(
    binary: str,
    prompt: str,
    permission_mode: str,
    allowed_tools: List[str],
    bare: bool,
) -> List[str]:
    if permission_mode not in SAFE_PERMISSION_MODES:
        allowed = ", ".join(sorted(SAFE_PERMISSION_MODES))
        raise AdapterError(f"permission_mode must be one of: {allowed}")
    if any(not _nonempty_string(tool) for tool in allowed_tools):
        raise AdapterError("allowed tools must be non-empty strings")

    command = [binary]
    if bare:
        command.append("--bare")
    command.extend(
        [
            "-p",
            prompt,
            "--output-format",
            "json",
            "--json-schema",
            json.dumps(RESULT_SCHEMA, separators=(",", ":")),
            "--permission-mode",
            permission_mode,
        ]
    )
    if allowed_tools:
        command.extend(["--allowedTools", ",".join(allowed_tools)])
    return command


def normalize_response(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get("structured_output"), dict):
        raise AdapterError("Claude Code response did not contain a structured_output object")
    result = payload["structured_output"]
    if result.get("status") not in {"completed", "blocked", "failed"}:
        raise AdapterError("structured_output.status is invalid")
    if not _nonempty_string(result.get("summary")):
        raise AdapterError("structured_output.summary must be a non-empty string")
    for field in sorted(RESULT_LIST_FIELDS):
        value = result.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise AdapterError(f"structured_output.{field} must be an array of strings")
    return {key: result[key] for key in RESULT_SCHEMA["required"]}


def run_agent(
    task: Dict[str, Any],
    binary: str,
    permission_mode: str,
    allowed_tools: List[str],
    bare: bool,
    timeout_seconds: int,
) -> Dict[str, Any]:
    normalized_task = validate_task(task)
    validate_execution_policy(normalized_task, permission_mode, allowed_tools)
    if timeout_seconds < 1:
        raise AdapterError("timeout must be at least one second")
    resolved_binary = resolve_binary(binary)
    command = build_command(
        binary=resolved_binary,
        prompt=build_prompt(),
        permission_mode=permission_mode,
        allowed_tools=allowed_tools,
        bare=bare,
    )
    try:
        process = subprocess.run(
            command,
            cwd=normalized_task["workspace"],
            check=False,
            capture_output=True,
            text=True,
            input=json.dumps(normalized_task, ensure_ascii=False),
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise AdapterError(f"Claude Code run timed out after {timeout_seconds} seconds") from exc
    if process.returncode != 0:
        detail = (process.stderr or process.stdout or "unknown error").strip()[:ERROR_DETAIL_LIMIT]
        raise AdapterError(f"Claude Code exited with {process.returncode}: {detail}")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise AdapterError("Claude Code returned invalid JSON") from exc
    return normalize_response(payload)


def _load_task(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"could not read task file: {exc}") from exc


def _failure_result(message: str, bare: bool = False) -> Dict[str, Any]:
    lowered = message.lower()
    result: Dict[str, Any] = {
        "status": "failed",
        "summary": message,
        "changed_artifacts": [],
        "validation_results": [],
        "risks": [],
        "assumptions": [],
        "unresolved": [message],
    }
    if "authentication" in lowered or "not logged in" in lowered or "login" in lowered:
        if bare:
            result["requires_user_action"] = (
                "Configure `ANTHROPIC_API_KEY` or the selected provider credentials for bare "
                "mode, or rerun without `--bare` to use an existing Claude Code login."
            )
        else:
            result["requires_user_action"] = (
                "Run `claude` interactively in a terminal and complete `/login`, then rerun."
            )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("preflight", help="check the binary and workspace")
    check.add_argument("--workspace", required=True)
    check.add_argument("--claude-bin", default="claude")

    run = subparsers.add_parser("run", help="execute one task contract")
    run.add_argument("--task-file", required=True)
    run.add_argument("--claude-bin", default="claude")
    run.add_argument("--permission-mode", choices=sorted(SAFE_PERMISSION_MODES), default="dontAsk")
    run.add_argument("--allowed-tool", action="append", default=[])
    run.add_argument("--bare", action="store_true")
    run.add_argument("--timeout", type=int, default=DEFAULT_RUN_TIMEOUT_SECONDS)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "preflight":
            result = preflight(args.claude_bin, args.workspace)
        else:
            result = run_agent(
                task=_load_task(args.task_file),
                binary=args.claude_bin,
                permission_mode=args.permission_mode,
                allowed_tools=args.allowed_tool,
                bare=args.bare,
                timeout_seconds=args.timeout,
            )
    except AdapterError as exc:
        print(
            json.dumps(
                _failure_result(str(exc), bare=getattr(args, "bare", False)),
                ensure_ascii=False,
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
