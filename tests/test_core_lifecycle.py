from __future__ import annotations

import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from harneloop.adapters import export_unit
from harneloop.attempts import add_attempt_observation, conclude_attempt, create_attempt_plan
from harneloop.candidate import create_candidate, list_candidates, rebase_candidate, set_candidate_status
from harneloop.diagnostics import run_doctor
from harneloop.environment import connect_environment, render_environment_status
from harneloop.errors import HarneloopError
from harneloop.evidence import add_evidence, list_evidence
from harneloop.intake import acknowledge_intake, read_intake, render_intake_markdown, resolve_intake_field
from harneloop.onboarding import render_onboarding_json, render_onboarding_markdown
from harneloop.packaging import package_unit
from harneloop.runs import add_artifact, finish_run, start_run
from harneloop.state import (
    build_session_brief_data,
    mark_active,
    mark_stopped,
    mark_waiting,
    read_state,
    render_session_brief_markdown,
    render_state_markdown,
)
from harneloop.target import set_target_brief
from harneloop.templates import list_templates
from harneloop.unit import init_unit, upgrade_unit_protocol
from harneloop.validation import validate_unit
from harneloop.versioning import promote_candidate, rollback_unit
from harneloop.yamlio import read_yaml, write_yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class CoreLifecycleTests(unittest.TestCase):
    def _acknowledge_test_intake(self, unit: Path) -> None:
        acknowledge_intake(unit, basis="user_delegated", note="Test delegates setup context.")

    def test_new_unit_requires_adaptive_intake_before_first_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            intake = read_intake(unit)

            self.assertEqual(intake["status"], "pending")
            self.assertEqual(intake["policy"], "adaptive")
            self.assertEqual(intake["fields"]["harness_goal"]["status"], "unknown")
            self.assertIn("questions that still matter", render_intake_markdown(intake))
            with self.assertRaisesRegex(HarneloopError, "intake checkpoint"):
                start_run(unit, task="Premature baseline")

    def test_existing_unit_can_adopt_new_protocol_without_overwriting_material(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            (unit / ".evolve" / "intake.yaml").unlink()
            (unit / ".evolve" / "SESSION_BRIEF.md").unlink()
            (unit / "AGENTS.md").unlink()
            custom = unit / "agent-facing" / "custom.md"
            custom.write_text("keep me\n", encoding="utf-8")

            created = upgrade_unit_protocol(unit)
            second_run = upgrade_unit_protocol(unit)

            self.assertEqual(sorted(created), [".evolve/SESSION_BRIEF.md", ".evolve/intake.yaml", "AGENTS.md"])
            self.assertEqual(second_run, [])
            self.assertEqual(custom.read_text(encoding="utf-8"), "keep me\n")
            self.assertEqual(read_intake(unit)["status"], "pending")

    def test_intake_can_record_inference_and_explicit_user_delegation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            resolve_intake_field(
                unit,
                "harness_goal",
                value="Improve responsive interface reproduction",
                status="inferred",
                source="initial user prompt",
            )
            ready = acknowledge_intake(
                unit,
                basis="user_delegated",
                note="User asked the agent to propose the remaining validation details.",
            )

            self.assertEqual(ready["status"], "ready")
            self.assertEqual(ready["acknowledgement"]["basis"], "user_delegated")
            self.assertEqual(ready["fields"]["harness_goal"]["status"], "inferred")
            self.assertEqual(start_run(unit, task="Delegated baseline").name, "run-0001")

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
            set_candidate_status(unit, "cand-0001", "ready")

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
            set_candidate_status(unit, "cand-0001", "ready")

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
            set_candidate_status(unit, "cand-0001", "ready")
            promote_candidate(unit, "cand-0001", "0.1.0")

            second = create_candidate(unit, "Revise principle")
            second_change = second / "changes" / "agent-facing" / "principles.md"
            second_change.parent.mkdir(parents=True, exist_ok=True)
            second_change.write_text("revised\n", encoding="utf-8")
            add_evidence(unit, "cand-0002", kind="manual_review", summary="Revised principle evidence")
            set_candidate_status(unit, "cand-0002", "ready")
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

            scoped_rules = (unit / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("When work concerns this harness unit", scoped_rules)
            self.assertIn("SESSION_BRIEF.md", scoped_rules)
            self.assertNotIn("entire agent session", scoped_rules)

            session_brief = (unit / ".evolve" / "SESSION_BRIEF.md").read_text(encoding="utf-8")
            self.assertIn("Harneloop Unit Brief", session_brief)
            self.assertIn("When working on this unit", session_brief)
            self.assertIn("Intake: `pending`", session_brief)

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

    def test_parallel_candidates_remain_active_and_agent_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")

            create_candidate(
                unit,
                "Accumulate spatial tools",
                plane="target_harness",
                validation_tier="representative",
            )
            create_candidate(
                unit,
                "Repair visual comparison",
                plane="evaluation",
                validation_tier="targeted",
            )

            state = read_state(unit)
            self.assertEqual(state["active_candidates"], ["cand-0001", "cand-0002"])
            self.assertEqual(state["active_candidate"], "cand-0002")
            candidates = list_candidates(unit, include_closed=False)
            self.assertEqual([item["id"] for item in candidates], ["cand-0001", "cand-0002"])
            self.assertEqual(candidates[0]["status"], "accumulating")
            self.assertEqual(candidates[0]["plane"], "target_harness")
            self.assertEqual(candidates[1]["plane"], "evaluation")

            allowed = read_yaml(unit / ".evolve" / "allowed-edits.yaml")
            self.assertIn("candidates/cand-0001/**", allowed["allowed_paths"])
            self.assertIn("candidates/cand-0002/**", allowed["allowed_paths"])
            brief = render_session_brief_markdown(build_session_brief_data(unit))
            self.assertIn("cand-0001", brief)
            self.assertIn("cand-0002", brief)
            self.assertIn("representative", brief)

    def test_candidate_validation_tier_controls_promotion_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            candidate = create_candidate(
                unit,
                "Improve environment startup",
                plane="infrastructure",
                validation_tier="targeted",
            )
            change = candidate / "changes" / "environment" / "startup.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("startup contract\n", encoding="utf-8")
            report = root / "structural-check.txt"
            report.write_text("schema valid\n", encoding="utf-8")
            add_evidence(
                unit,
                "cand-0001",
                kind="structural_check",
                summary="The configuration parses.",
                path=report,
                validation_tier="structural",
            )
            set_candidate_status(unit, "cand-0001", "ready")

            with self.assertRaisesRegex(HarneloopError, "targeted"):
                promote_candidate(unit, "cand-0001", "0.1.0")

            self._acknowledge_test_intake(unit)
            start_run(unit, task="Smoke-test startup", candidate_id="cand-0001")
            finish_run(unit, "run-0001", status="succeeded", summary="Startup smoke passed")
            add_evidence(
                unit,
                "cand-0001",
                kind="smoke_test",
                summary="The environment started successfully.",
                run_id="run-0001",
                validation_tier="targeted",
            )

            version = promote_candidate(unit, "cand-0001", "0.1.0")
            self.assertTrue(version.exists())
            version_meta = read_yaml(version / "version.yaml")
            self.assertEqual(version_meta["plane"], "infrastructure")
            self.assertEqual(version_meta["validation_tier"], "targeted")

    def test_parallel_candidate_requires_rebase_and_fresh_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            first = create_candidate(unit, "First batch", plane="infrastructure", validation_tier="structural")
            second = create_candidate(unit, "Second batch", plane="evaluation", validation_tier="structural")
            for candidate, name in [(first, "first.md"), (second, "second.md")]:
                change = candidate / "changes" / "tools" / name
                change.parent.mkdir(parents=True, exist_ok=True)
                change.write_text(name, encoding="utf-8")

            report = root / "check.txt"
            report.write_text("valid\n", encoding="utf-8")
            for candidate_id in ["cand-0001", "cand-0002"]:
                add_evidence(
                    unit,
                    candidate_id,
                    kind="structural_check",
                    summary="The candidate structure is valid.",
                    path=report,
                    validation_tier="structural",
                )
                set_candidate_status(unit, candidate_id, "ready")

            promote_candidate(unit, "cand-0001", "0.1.0")
            second_meta = read_yaml(second / "candidate.yaml")
            self.assertEqual(second_meta["status"], "needs_rebase")
            self.assertEqual(read_state(unit)["active_candidates"], ["cand-0002"])
            self._acknowledge_test_intake(unit)
            with self.assertRaisesRegex(HarneloopError, "cannot be tested"):
                start_run(unit, task="Test stale candidate", candidate_id="cand-0002")
            with self.assertRaisesRegex(HarneloopError, "rebase"):
                promote_candidate(unit, "cand-0002", "0.2.0")

            rebased = rebase_candidate(unit, "cand-0002")
            self.assertEqual(rebased["base_version"], "0.1.0")
            self.assertEqual(rebased["status"], "accumulating")
            set_candidate_status(unit, "cand-0002", "ready")
            with self.assertRaisesRegex(HarneloopError, "fresh evidence"):
                promote_candidate(unit, "cand-0002", "0.2.0")

            add_evidence(
                unit,
                "cand-0002",
                kind="structural_check",
                summary="The rebased candidate remains valid.",
                path=report,
                validation_tier="structural",
            )
            promoted = promote_candidate(unit, "cand-0002", "0.2.0")
            self.assertTrue(promoted.exists())
            self.assertEqual(read_state(unit)["active_candidates"], [])

    def test_representative_evidence_requires_a_recorded_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            create_candidate(unit, "Change tool behavior", plane="target_harness", validation_tier="representative")
            report = root / "review.md"
            report.write_text("looks good\n", encoding="utf-8")

            with self.assertRaisesRegex(HarneloopError, "recorded run"):
                add_evidence(
                    unit,
                    "cand-0001",
                    kind="artifact_review",
                    summary="Unlinked visual review.",
                    path=report,
                    validation_tier="representative",
                )

    def test_legacy_candidate_retains_original_promotion_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            candidate = create_candidate(unit, "Legacy change")
            candidate_meta_path = candidate / "candidate.yaml"
            candidate_meta = read_yaml(candidate_meta_path)
            candidate_meta.pop("schema_version")
            candidate_meta.pop("plane")
            candidate_meta.pop("validation_tier")
            candidate_meta["status"] = "draft"
            write_yaml(candidate_meta_path, candidate_meta)

            change = candidate / "changes" / "agent-facing" / "principles.md"
            change.parent.mkdir(parents=True, exist_ok=True)
            change.write_text("legacy guidance\n", encoding="utf-8")
            add_evidence(unit, "cand-0001", kind="manual_review", summary="Legacy evidence")

            promoted = promote_candidate(unit, "cand-0001", "0.1.0")
            self.assertTrue(promoted.exists())

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
            self._acknowledge_test_intake(unit)
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
            self._acknowledge_test_intake(unit)
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
            self._acknowledge_test_intake(unit)
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

            self._acknowledge_test_intake(unit)
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

            self._acknowledge_test_intake(unit)
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
            set_candidate_status(unit, "cand-0001", "ready")
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
            set_candidate_status(unit, "cand-0001", "ready")

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
            set_candidate_status(unit, "cand-0001", "ready")
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

            self._acknowledge_test_intake(unit)
            run_root = start_run(unit, task="Generate a task artifact", attempt_id="attempt-0001")
            run_record = read_yaml(run_root / "run.yaml")
            self.assertEqual(run_record["attempt_id"], "attempt-0001")

    def test_finished_attempt_requires_evaluation_before_next_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            self._acknowledge_test_intake(unit)
            create_attempt_plan(
                unit,
                goal="Reproduce a reference interface",
                method="Render and compare the result.",
                expected_artifact=["reference_screenshot", "candidate_screenshot", "visual_review_notes"],
            )
            start_run(unit, task="Baseline", attempt_id="attempt-0001")
            for name, kind in [("reference.png", "reference_screenshot"), ("candidate.png", "candidate_screenshot")]:
                artifact = root / name
                artifact.write_bytes(name.encode("utf-8"))
                add_artifact(unit, "run-0001", artifact, kind=kind)
            finish_run(unit, "run-0001", status="succeeded", summary="Execution completed")

            self.assertEqual(read_state(unit)["state"], "awaiting_evaluation")
            with self.assertRaisesRegex(HarneloopError, "missing expected artifacts"):
                conclude_attempt(
                    unit,
                    "attempt-0001",
                    run_id="run-0001",
                    outcome="pass",
                    decision="accept",
                    summary="Looks good enough.",
                    confidence="high",
                )

            conclusion = conclude_attempt(
                unit,
                "attempt-0001",
                run_id="run-0001",
                outcome="partial",
                decision="request_input",
                summary="Desktop evidence is good, but responsive references are missing.",
                confidence="medium",
                question="Please provide the tablet and mobile reference images.",
            )
            self.assertEqual(conclusion["missing_expected_artifacts"], ["visual_review_notes"])
            self.assertEqual(read_state(unit)["state"], "waiting")
            self.assertIn("tablet and mobile", read_state(unit)["next_action"])

    def test_good_first_attempt_can_be_accepted_without_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "unit", "demo", "Demo Unit")
            self._acknowledge_test_intake(unit)
            create_attempt_plan(
                unit,
                goal="Generate a useful result",
                method="Produce and inspect the result.",
                expected_artifact=["result", "review"],
            )
            start_run(unit, task="Baseline", attempt_id="attempt-0001")
            for name, kind in [("result.txt", "result"), ("review.txt", "review")]:
                artifact = root / name
                artifact.write_text(name, encoding="utf-8")
                add_artifact(unit, "run-0001", artifact, kind=kind)
            finish_run(unit, "run-0001", status="succeeded", summary="Execution completed")

            conclusion = conclude_attempt(
                unit,
                "attempt-0001",
                run_id="run-0001",
                outcome="pass",
                decision="accept",
                summary="The current harness is effective enough for this test; no change is justified.",
                confidence="high",
            )

            self.assertEqual(conclusion["decision"], "accept")
            self.assertEqual(conclusion["missing_expected_artifacts"], [])
            self.assertEqual(read_state(unit)["state"], "satisfied")
            self.assertIsNone(read_state(unit)["active_candidate"])
            brief_data = build_session_brief_data(unit)
            brief_markdown = render_session_brief_markdown(brief_data)
            self.assertEqual(brief_data["latest_conclusion"]["decision"], "accept")
            self.assertIn("No candidate is needed", brief_markdown)
            self.assertIn("Generate a useful result", brief_markdown)

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
        self.assertIn("harneloop intake status", markdown)
        self.assertIn("do not silently convert", markdown)
        self.assertIn("harneloop attempt conclude", markdown)
        self.assertIn("coherent change batch", markdown)
        self.assertIn("multiple candidates open", markdown)
        self.assertIn("structural for metadata", markdown)
        self.assertIn("execution success", markdown.lower())
        self.assertTrue((REPO_ROOT / "skills" / "harneloop" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
