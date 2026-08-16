import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import claude_code_adapter as adapter


def task_contract(workspace: str) -> dict:
    return {
        "contract_version": "1",
        "goal": "Inspect README.md and report its first heading.",
        "workspace": workspace,
        "allowed_scope": ["README.md"],
        "allowed_actions": ["read"],
        "prohibited_actions": ["modify_files", "external_write"],
        "acceptance_criteria": ["Return the exact first heading."],
        "validation": ["Read README.md directly."],
        "required_report": "executor-result-v1",
    }


def completed_result() -> dict:
    return {
        "status": "completed",
        "summary": "The first heading is # Demo.",
        "changed_artifacts": [],
        "validation_results": ["Read README.md: pass"],
        "risks": [],
        "assumptions": [],
        "unresolved": [],
    }


def write_fake_cli(path: Path, help_text: str) -> None:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        "if '--version' in sys.argv:\n"
        "    print('2.1.231 (Claude Code)')\n"
        "else:\n"
        f"    print({help_text!r})\n",
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


class ClaudeCodeAdapterTests(unittest.TestCase):
    def test_validate_task_rejects_missing_required_field(self):
        with tempfile.TemporaryDirectory() as workspace:
            task = task_contract(workspace)
            del task["acceptance_criteria"]
            with self.assertRaisesRegex(adapter.AdapterError, "acceptance_criteria"):
                adapter.validate_task(task)

    def test_validate_task_rejects_empty_scope(self):
        with tempfile.TemporaryDirectory() as workspace:
            task = task_contract(workspace)
            task["allowed_scope"] = []
            with self.assertRaisesRegex(adapter.AdapterError, "allowed_scope"):
                adapter.validate_task(task)

    def test_validate_task_requires_absolute_workspace(self):
        task = task_contract(".")
        with self.assertRaisesRegex(adapter.AdapterError, "absolute"):
            adapter.validate_task(task)

    def test_build_command_is_locked_down_and_structured(self):
        command = adapter.build_command(
            binary="claude",
            prompt="do the task",
            permission_mode="dontAsk",
            allowed_tools=["Read", "Bash(git status *)"],
            bare=False,
        )

        self.assertEqual(command[0:3], ["claude", "-p", "do the task"])
        self.assertIn("--output-format", command)
        self.assertIn("--json-schema", command)
        self.assertEqual(command[command.index("--permission-mode") + 1], "dontAsk")
        self.assertEqual(
            command[command.index("--allowedTools") + 1],
            "Read,Bash(git status *)",
        )
        self.assertNotIn("bypassPermissions", command)

    def test_normalize_requires_structured_output(self):
        with self.assertRaisesRegex(adapter.AdapterError, "structured_output"):
            adapter.normalize_response({"result": "plain text"})

    def test_read_only_task_rejects_edit_tool(self):
        with tempfile.TemporaryDirectory() as workspace:
            task = adapter.validate_task(task_contract(workspace))
            with self.assertRaisesRegex(adapter.AdapterError, "modify_files"):
                adapter.validate_execution_policy(task, "dontAsk", ["Read", "Edit"])

    def test_read_only_task_rejects_accept_edits_mode(self):
        with tempfile.TemporaryDirectory() as workspace:
            task = adapter.validate_task(task_contract(workspace))
            with self.assertRaisesRegex(adapter.AdapterError, "acceptEdits"):
                adapter.validate_execution_policy(task, "acceptEdits", ["Read"])

    def test_run_agent_with_fake_claude(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "README.md").write_text("# Demo\n", encoding="utf-8")

            fake = root / "fake-claude"
            payload = json.dumps({"structured_output": completed_result()})
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json, sys\n"
                "task = json.load(sys.stdin)\n"
                "assert task['goal'].startswith('Inspect README.md')\n"
                f"print({payload!r})\n",
                encoding="utf-8",
            )
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR)

            result = adapter.run_agent(
                task=task_contract(str(workspace)),
                binary=str(fake),
                permission_mode="dontAsk",
                allowed_tools=["Read"],
                bare=False,
                timeout_seconds=30,
            )

            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["changed_artifacts"], [])

    def test_preflight_reports_binary_and_workspace(self):
        required_help = " ".join(adapter.REQUIRED_CLI_OPTIONS) + " --bare"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            fake = root / "fake-claude"
            write_fake_cli(fake, required_help)
            report = adapter.preflight(str(fake), str(workspace))
        self.assertTrue(report["ok"])
        self.assertEqual(report["workspace"], str(workspace.resolve()))
        self.assertTrue(report["version"])
        self.assertEqual(report["required_options"], "supported")
        self.assertTrue(report["supports_bare"])

    def test_preflight_rejects_cli_without_structured_output_flag(self):
        incomplete_help = "--print --output-format --permission-mode --allowedTools"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            fake = root / "fake-claude"
            write_fake_cli(fake, incomplete_help)
            with self.assertRaisesRegex(adapter.AdapterError, "--json-schema"):
                adapter.preflight(str(fake), str(workspace))

    def test_bare_auth_failure_names_bare_mode_credentials(self):
        result = adapter._failure_result("authentication failed", bare=True)
        self.assertIn("ANTHROPIC_API_KEY", result["requires_user_action"])

    def test_non_bare_auth_failure_names_interactive_login(self):
        result = adapter._failure_result("not logged in", bare=False)
        self.assertIn("/login", result["requires_user_action"])


if __name__ == "__main__":
    unittest.main()
