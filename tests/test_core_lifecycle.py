from __future__ import annotations

import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from harneloop.adapters import export_unit
from harneloop.attempts import add_attempt_observation, create_attempt_plan
from harneloop.candidate import create_candidate
from harneloop.diagnostics import run_doctor
from harneloop.environment import connect_environment, render_environment_status
from harneloop.errors import HarneloopError
from harneloop.evidence import add_evidence, list_evidence
from harneloop.onboarding import render_onboarding_json, render_onboarding_markdown
from harneloop.packaging import package_unit
from harneloop.runs import add_artifact, finish_run, start_run
from harneloop.state import mark_active, mark_stopped, mark_waiting, read_state, render_state_markdown
from harneloop.target import set_target_brief
from harneloop.templates import list_templates
from harneloop.unit import init_unit
from harneloop.validation import validate_unit
from harneloop.versioning import promote_candidate, rollback_unit
from harneloop.yamlio import read_yaml


class CoreLifecycleTests(unittest.TestCase):
    def test_create_candidate_promote_snapshot_and_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            create_attempt_plan(
                unit,
                goal="Create a first task artifact",
                method="Use agent capabilities to produce an artifact.",
            )
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
            self.assertTrue(any(name.endswith("HARNELOOP_PACKAGE.json") for name in names))
            self.assertTrue(any(name.endswith("operational-map.md") for name in names))
            self.assertTrue(any(name.endswith("agent-facing/principles.md") for name in names))
            self.assertFalse(any("/attempts/" in name for name in names))

    def test_candidate_cannot_modify_protected_unit_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Attempt protected edit")
            (candidate / "changes" / "unit.yaml").write_text("id: changed\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Protected edit test evidence")

            with self.assertRaises(HarneloopError):
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

    def test_init_unit_creates_operational_map_for_agent_navigation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            map_path = unit / "operational-map.md"

            self.assertTrue(map_path.exists())
            content = map_path.read_text(encoding="utf-8")
            self.assertIn("Use this map as current orientation.", content)
            self.assertIn("This is context and navigation, not a rigid procedure.", content)
            self.assertIn("What This Harness Unit Is Trying To Improve", content)
            self.assertIn("Systems, Tools, And Environment", content)
            self.assertIn("Useful Artifacts And Evidence", content)
            self.assertIn("Running And Resetting The Environment", content)
            self.assertIn("Automation And Autonomy", content)
            self.assertIn("Capability Gaps", content)
            self.assertIn("Operating-agent capabilities currently available", content)
            self.assertIn("Missing operating-agent capabilities", content)
            self.assertIn("Unit or target-agent tools", content)
            self.assertIn("Requested or enabled tools", content)
            self.assertIn("Fallbacks if the user declines", content)
            self.assertIn("Capability additions should be justified", content)
            self.assertIn("Existing Work And Reuse", content)
            self.assertIn("best verified result, not a from-scratch implementation", content)
            self.assertIn("License, attribution, compatibility, security, cost, and permission notes", content)
            self.assertIn("Known Constraints, Fragile Spots, And Open Questions", content)
            self.assertIn("Current Assumptions To Re-Check", content)
            self.assertIn("Prior Runs, Evidence, And Decisions", content)
            self.assertFalse(validate_unit(unit))

            forbidden_phrases = [
                "Always evaluate success by these exact criteria",
                "The loop must be run in this exact order",
                "A harness change helped only if X/Y/Z",
                "Use these artifacts for every task",
            ]
            for phrase in forbidden_phrases:
                self.assertNotIn(phrase, content)

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

    def test_finished_run_rejects_artifacts_and_second_finish(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            run_root = start_run(unit, task="Create a simple artifact")
            finish_run(unit, "run-0001", status="succeeded", summary="Original result")

            artifact_source = root / "late-artifact.txt"
            artifact_source.write_text("late artifact\n", encoding="utf-8")
            with self.assertRaisesRegex(HarneloopError, "already finished"):
                add_artifact(unit, "run-0001", artifact_source, kind="text")
            with self.assertRaisesRegex(HarneloopError, "already finished"):
                finish_run(unit, "run-0001", status="failed", summary="Overwritten result")

            run_record = read_yaml(run_root / "run.yaml")
            self.assertEqual(run_record["status"], "succeeded")
            self.assertEqual(run_record["summary"], "Original result")
            self.assertEqual(run_record["artifacts"], [])

    def test_candidate_evidence_records_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            create_candidate(unit, "Add evidence-backed change")
            start_run(unit, task="Render the artifact")
            artifact_source = root / "render.png"
            artifact_source.write_bytes(b"rendered artifact")
            add_artifact(unit, "run-0001", artifact_source, kind="image")

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

    def test_candidate_evidence_rejects_missing_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            create_candidate(unit, "Add evidence-backed change")

            with self.assertRaisesRegex(HarneloopError, "Run does not exist"):
                add_evidence(
                    unit,
                    "cand-0001",
                    kind="artifact_review",
                    summary="References a missing run.",
                    run_id="run-9999",
                )
            with self.assertRaisesRegex(HarneloopError, "requires a run_id"):
                add_evidence(
                    unit,
                    "cand-0001",
                    kind="artifact_review",
                    summary="Artifact has no owning run.",
                    artifact_id="artifact-0001",
                )

            start_run(unit, task="Render the artifact")
            with self.assertRaisesRegex(HarneloopError, "Artifact does not exist"):
                add_evidence(
                    unit,
                    "cand-0001",
                    kind="artifact_review",
                    summary="References a missing artifact.",
                    run_id="run-0001",
                    artifact_id="artifact-9999",
                )
            with self.assertRaisesRegex(HarneloopError, "Evidence file does not exist"):
                add_evidence(
                    unit,
                    "cand-0001",
                    kind="report",
                    summary="References a missing report.",
                    path=root / "missing-report.md",
                )

            self.assertEqual(list_evidence(unit, "cand-0001"), [])

    def test_promotion_revalidates_evidence_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Add evidence-backed change")
            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("inspect artifacts\n", encoding="utf-8")

            start_run(unit, task="Render the artifact")
            artifact_source = root / "render.png"
            artifact_source.write_bytes(b"rendered artifact")
            artifact = add_artifact(unit, "run-0001", artifact_source, kind="image")
            add_evidence(
                unit,
                "cand-0001",
                kind="artifact_review",
                summary="The render supports this change.",
                run_id="run-0001",
                artifact_id=artifact["id"],
            )
            (unit / artifact["stored_path"]).unlink()

            with self.assertRaisesRegex(HarneloopError, "stored file does not exist"):
                promote_candidate(unit, "cand-0001", "0.1.0")
            self.assertFalse((unit / "versions" / "0.1.0").exists())

    def test_promotion_requires_evidence_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Try unevidenced change")
            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("needs evidence\n", encoding="utf-8")

            with self.assertRaises(HarneloopError):
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
            self.assertTrue((cursor_export / "harneloop-unit.mdc").exists())
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
            self.assertIn("Harneloop records the mapping", getting_started)

    def test_agent_attempt_plan_records_custom_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            attempt = create_attempt_plan(
                unit,
                goal="Build a Blender scene with a cube on a table and a visible camera view.",
                method="Use the existing Blender MCP tools to create objects, render, and export a scene summary.",
                action=[
                    "Create table, cube, camera, and light with MCP tools.",
                    "Render the scene and capture a screenshot.",
                    "Export object transforms and camera visibility summary.",
                ],
                expected_artifact=["render", "screenshot", "scene_summary"],
                success_check=["Cube rests on table", "All required objects are visible to camera"],
                note=["There is no single test command; the agent performs this workflow through tools."],
            )

            self.assertEqual(attempt["id"], "attempt-0001")
            self.assertIn("render", attempt["expected_artifacts"])
            self.assertTrue((unit / "attempts" / "attempt-0001" / "attempt.yaml").exists())

            observation = add_attempt_observation(
                unit,
                "attempt-0001",
                summary="Render exists but cube is floating above the table.",
                outcome="failed",
                run_id="run-0001",
                finding=["Likely z-coordinate placement issue"],
            )
            self.assertEqual(observation["outcome"], "failed")
            observations = (unit / "attempts" / "attempt-0001" / "OBSERVATIONS.md").read_text(encoding="utf-8")
            self.assertIn("floating above the table", observations)

    def test_run_can_link_to_agent_attempt_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            create_attempt_plan(
                unit,
                goal="Generate a task artifact",
                method="Use agent tools to create the artifact.",
            )

            run_root = start_run(unit, task="Generate a task artifact", attempt_id="attempt-0001")
            run_record = read_yaml(run_root / "run.yaml")
            self.assertEqual(run_record["attempt_id"], "attempt-0001")

    def test_agent_onboarding_collects_minimal_context(self) -> None:
        data = render_onboarding_json()
        markdown = render_onboarding_markdown()

        self.assertLessEqual(data["question_limit"], 5)
        question_ids = {item["id"] for item in data["questions"]}
        self.assertIn("harness_goal", question_ids)
        self.assertIn("success_strategy", question_ids)
        self.assertIn("validation_preference", question_ids)
        self.assertIn("environment_status", question_ids)
        self.assertIn("What should this harness help an agent get better at", markdown)
        self.assertIn("How should results be validated", markdown)
        self.assertIn("best validation quality", markdown)
        self.assertIn("harneloop target set", markdown)
        self.assertIn("harneloop environment connect", markdown)
        self.assertIn("--interaction-mode mcp", markdown)
        self.assertIn("does not discover environment endpoints", markdown)
        self.assertIn("operational-map.md", markdown)
        self.assertIn("automating the environment is reasonable", markdown)
        self.assertIn("Operating-agent capabilities", markdown)
        self.assertIn("Unit/target-agent tools", markdown)
        self.assertIn("Capability additions should be justified", markdown)
        self.assertIn("best verified result, not a from-scratch implementation", markdown)
        self.assertIn("Record the source, relevant version, purpose", markdown)


if __name__ == "__main__":
    unittest.main()
