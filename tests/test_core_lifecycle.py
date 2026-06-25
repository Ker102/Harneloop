from __future__ import annotations

import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from evorig.adapters import export_unit
from evorig.candidate import create_candidate
from evorig.diagnostics import run_doctor
from evorig.environment import connect_environment, render_environment_status
from evorig.errors import EvoRigError
from evorig.evidence import add_evidence, list_evidence
from evorig.packaging import package_unit
from evorig.runs import add_artifact, finish_run, start_run
from evorig.state import mark_active, mark_stopped, mark_waiting, read_state, render_state_markdown
from evorig.target import set_target_brief
from evorig.templates import list_templates
from evorig.unit import init_unit
from evorig.versioning import promote_candidate, rollback_unit
from evorig.yamlio import read_yaml


class CoreLifecycleTests(unittest.TestCase):
    def test_create_candidate_promote_snapshot_and_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Add first task principle")
            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("# Principles\n\nCheck real artifacts before promotion.\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Smoke-test evidence")

            version_root = promote_candidate(unit, "cand-0001", "0.1.0")

            self.assertTrue((unit / "agent-facing" / "principles.md").exists())
            self.assertTrue((version_root / "snapshot" / "agent-facing" / "principles.md").exists())
            self.assertEqual(read_yaml(unit / "unit.yaml")["current_version"], "0.1.0")

            package_path = package_unit(unit, Path(temp_dir) / "demo.tar.gz")
            self.assertTrue(package_path.exists())
            with tarfile.open(package_path, "r:gz") as archive:
                names = archive.getnames()
            self.assertTrue(any(name.endswith("EVORIG_PACKAGE.json") for name in names))
            self.assertTrue(any(name.endswith("agent-facing/principles.md") for name in names))

    def test_candidate_cannot_modify_protected_unit_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Attempt protected edit")
            (candidate / "changes" / "unit.yaml").write_text("id: changed\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Protected edit test evidence")

            with self.assertRaises(EvoRigError):
                promote_candidate(unit, "cand-0001", "0.1.0")

    def test_rollback_restores_previous_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            first = create_candidate(unit, "Add original principle")
            first_change = first / "changes" / "agent-facing" / "principles.md"
            first_change.parent.mkdir(parents=True, exist_ok=True)
            first_change.write_text("original\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Original principle evidence")
            promote_candidate(unit, "cand-0001", "0.1.0")

            second = create_candidate(unit, "Revise principle")
            second_change = second / "changes" / "agent-facing" / "principles.md"
            second_change.parent.mkdir(parents=True, exist_ok=True)
            second_change.write_text("revised\n", encoding="utf-8")
            add_evidence(unit, "cand-0002", kind="manual_review", summary="Revised principle evidence")
            promote_candidate(unit, "cand-0002", "0.2.0")

            rollback_unit(unit, "0.1.0")

            self.assertEqual((unit / "agent-facing" / "principles.md").read_text(encoding="utf-8"), "original\n")
            self.assertEqual(read_state(unit)["current_version"], "0.1.0")

    def test_wait_stop_and_resume_state_are_resumable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")

            waiting = mark_waiting(
                unit,
                reason="delayed_artifact",
                next_action="inspect_artifact",
                resume_after="2026-06-25T18:00:00Z",
                resume_condition="runtime/artifacts/run-014/render.png exists",
            )
            self.assertEqual(waiting["state"], "waiting")
            self.assertEqual(read_state(unit)["next_action"], "inspect_artifact")
            self.assertIn("delayed_artifact", (unit / ".evolve" / "CURRENT_STATE.md").read_text(encoding="utf-8"))

            stopped = mark_stopped(unit, reason="capability_frontier_plateau")
            self.assertEqual(stopped["state"], "stopped")

            active = mark_active(unit, reason="manual_resume", next_action="create_candidate")
            self.assertEqual(active["state"], "active")
            self.assertEqual(active["next_action"], "create_candidate")

    def test_status_file_is_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            data = json.loads((unit / ".evolve" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(data["unit_id"], "demo")

    def test_artifact_review_template_seeds_unit_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit", template="artifact-review")

            self.assertIn("artifact-review", list_templates())
            self.assertTrue((unit / "agent-facing" / "principles.md").exists())
            self.assertTrue((unit / "observers" / "contracts.yaml").exists())
            self.assertTrue((unit / "validators" / "contracts.yaml").exists())
            self.assertTrue((unit / "regression-cases" / "artifact-smoke.yaml").exists())
            principles = (unit / "agent-facing" / "principles.md").read_text(encoding="utf-8")
            self.assertIn("Inspect real artifacts", principles)

    def test_state_markdown_is_agent_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            state = read_state(unit)
            markdown = render_state_markdown(state)

            self.assertIn("# Current State", markdown)
            self.assertIn("State:", markdown)
            self.assertIn("Next Action", markdown)

    def test_allowed_edits_contract_tracks_active_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            allowed_path = unit / ".evolve" / "allowed-edits.yaml"
            self.assertTrue(allowed_path.exists())
            initial = read_yaml(allowed_path)
            self.assertIsNone(initial["active_candidate"])
            self.assertIn("unit.yaml", initial["protected_paths"])

            create_candidate(unit, "Add candidate-scoped work")
            active = read_yaml(allowed_path)
            self.assertEqual(active["active_candidate"], "cand-0001")
            self.assertIn("candidates/cand-0001/**", active["allowed_paths"])

    def test_doctor_reports_core_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            checks = run_doctor(Path(temp_dir))
            names = {check.name for check in checks}
            self.assertIn("python", names)
            self.assertIn("pyyaml", names)
            self.assertIn("git", names)
            self.assertIn("writable_cwd", names)
            self.assertTrue(all(isinstance(check.ok, bool) for check in checks))

    def test_run_record_and_artifact_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            run_root = start_run(unit, task="Create a simple artifact")
            self.assertEqual(run_root.name, "run-0001")

            artifact_source = root / "render.txt"
            artifact_source.write_text("artifact output\n", encoding="utf-8")
            artifact = add_artifact(
                unit,
                "run-0001",
                artifact_source,
                kind="text",
                description="Smoke-test artifact",
            )

            self.assertTrue((unit / artifact["stored_path"]).exists())
            run_record = read_yaml(run_root / "run.yaml")
            self.assertEqual(run_record["status"], "running")
            self.assertEqual(run_record["artifacts"][0]["kind"], "text")
            self.assertEqual(run_record["artifacts"][0]["description"], "Smoke-test artifact")

            finished = finish_run(unit, "run-0001", status="succeeded", summary="Artifact captured")
            self.assertEqual(finished["status"], "succeeded")
            self.assertEqual(finished["summary"], "Artifact captured")

    def test_candidate_evidence_records_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            create_candidate(unit, "Add evidence-backed change")

            evidence = add_evidence(
                unit,
                "cand-0001",
                kind="artifact_review",
                summary="Rendered artifact matches the task.",
                run_id="run-0001",
                artifact_id="artifact-0001",
                outcome="supports",
            )

            self.assertEqual(evidence["id"], "evidence-0001")
            self.assertEqual(evidence["outcome"], "supports")
            records = list_evidence(unit, "cand-0001")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["summary"], "Rendered artifact matches the task.")

    def test_promotion_requires_evidence_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Try unevidenced change")
            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("needs evidence\n", encoding="utf-8")

            with self.assertRaises(EvoRigError):
                promote_candidate(unit, "cand-0001", "0.1.0")

            version_root = promote_candidate(unit, "cand-0001", "0.1.0", require_evidence=False)
            self.assertTrue(version_root.exists())

    def test_export_adapters_write_agent_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Add exported guidance")
            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("# Principles\n\nUse evidence gates.\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Export evidence")
            promote_candidate(unit, "cand-0001", "0.1.0")

            codex_export = export_unit(unit, adapter="codex")
            generic_export = export_unit(unit, adapter="generic")
            cursor_export = export_unit(unit, adapter="cursor")

            self.assertTrue((codex_export / "AGENTS.md").exists())
            self.assertTrue((generic_export / "UNIT_AGENT.md").exists())
            self.assertTrue((cursor_export / "evorig-unit.mdc").exists())
            self.assertIn("Use evidence gates.", (codex_export / "AGENTS.md").read_text(encoding="utf-8"))

    def test_target_brief_generates_starter_test_suggestions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            brief = set_target_brief(
                unit,
                task="Improve a Blender agent's spatial scene construction.",
                success="Objects are placed correctly and visible to the camera.",
                artifact_kind=["render", "scene_summary"],
                risk=["wrong coordinate assumptions", "objects outside camera view"],
            )

            self.assertEqual(brief["task"], "Improve a Blender agent's spatial scene construction.")
            self.assertTrue((unit / "target" / "brief.yaml").exists())
            suggestions = (unit / "target" / "TEST_SUGGESTIONS.md").read_text(encoding="utf-8")
            self.assertIn("render", suggestions)
            self.assertIn("objects outside camera view", suggestions)

    def test_existing_environment_contract_is_agent_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            contract = connect_environment(
                unit,
                name="Existing Blender project harness",
                mode="existing",
                description="Project already has Blender execution and screenshot capture.",
                run_command="python run_blender_test.py",
                artifact_path="outputs/render.png",
                notes=["Do not rebuild the environment unless checks fail."],
            )

            self.assertEqual(contract["mode"], "existing")
            self.assertTrue((unit / "environment" / "contract.yaml").exists())
            markdown = render_environment_status(unit)
            self.assertIn("Existing Blender project harness", markdown)
            self.assertIn("Connect to the existing environment", markdown)

    def test_mcp_tool_environment_contract_does_not_require_run_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            contract = connect_environment(
                unit,
                name="Existing Blender MCP environment",
                mode="existing",
                description="Agent interacts with Blender through an MCP server and addon tools.",
                interaction_mode="mcp",
                tool=["create_object", "render_scene", "capture_screenshot", "export_scene_summary"],
                artifact_path="outputs/renders/*.png",
                notes=["The agent should use MCP tools instead of looking for a single run command."],
            )

            self.assertIsNone(contract["run_command"])
            self.assertEqual(contract["interaction_mode"], "mcp")
            self.assertIn("render_scene", contract["tools"])
            markdown = render_environment_status(unit)
            self.assertIn("Tool interface: `mcp`", markdown)
            self.assertIn("Use the declared tools", markdown)
            getting_started = (unit / "environment" / "GETTING_STARTED.md").read_text(encoding="utf-8")
            self.assertIn("render_scene", getting_started)
            self.assertIn("baseline run", getting_started)


if __name__ == "__main__":
    unittest.main()
