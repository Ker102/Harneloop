from __future__ import annotations

import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from evorig.candidate import create_candidate
from evorig.diagnostics import run_doctor
from evorig.errors import EvoRigError
from evorig.packaging import package_unit
from evorig.runs import add_artifact, finish_run, start_run
from evorig.state import mark_active, mark_stopped, mark_waiting, read_state
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

            with self.assertRaises(EvoRigError):
                promote_candidate(unit, "cand-0001", "0.1.0")

    def test_rollback_restores_previous_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "unit", "demo", "Demo Unit")
            first = create_candidate(unit, "Add original principle")
            first_change = first / "changes" / "agent-facing" / "principles.md"
            first_change.parent.mkdir(parents=True, exist_ok=True)
            first_change.write_text("original\n", encoding="utf-8")
            promote_candidate(unit, "cand-0001", "0.1.0")

            second = create_candidate(unit, "Revise principle")
            second_change = second / "changes" / "agent-facing" / "principles.md"
            second_change.parent.mkdir(parents=True, exist_ok=True)
            second_change.write_text("revised\n", encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
