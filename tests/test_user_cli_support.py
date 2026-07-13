from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from harneloop.cli import main
from harneloop.environment import connect_environment
from harneloop.errors import HarneloopError
from harneloop.preferences import (
    DEFAULT_PREFERENCES,
    list_registered_units,
    load_preferences,
    register_unit,
    resolve_unit_reference,
    update_preference,
)
from harneloop.setup_flow import (
    HUMAN_MAIN_MENU,
    build_guided_setup_plan,
    suggest_artifact_kinds,
    unit_id_from_name,
)
from harneloop.unit import init_unit


class UserCliSupportTests(unittest.TestCase):
    def test_human_main_menu_covers_unit_settings_and_help_workflows(self) -> None:
        ids = {item["id"] for item in HUMAN_MAIN_MENU}
        labels = {item["label"] for item in HUMAN_MAIN_MENU}

        self.assertIn("create_unit", ids)
        self.assertIn("manage_units", ids)
        self.assertIn("continue_unit", ids)
        self.assertIn("review_unit", ids)
        self.assertIn("manage_settings", ids)
        self.assertIn("help", ids)
        self.assertIn("List and manage harness units", labels)
        self.assertIn("Continue an active harness unit", labels)

    def test_guided_setup_defaults_make_success_and_artifacts_optional(self) -> None:
        plan = build_guided_setup_plan(
            goal="Improve SVG generation quality for an agent",
            usage_context="Codex or Cursor coding-agent workflow",
            success_strategy="agent_proposes",
            validation_preference="best_quality",
            environment_status="not_sure",
            constraints="Ask before installing browser tooling.",
            unit_name="SVG Quality Harness",
        )

        self.assertEqual(plan["unit_id"], "svg-quality-harness")
        self.assertIn("agent should propose", plan["success"].lower())
        self.assertIn("rendered_image", plan["artifact_kinds"])
        self.assertIn("browser_screenshot", plan["artifact_kinds"])
        self.assertEqual(plan["environment_mode"], "assisted")
        self.assertEqual(plan["interaction_mode"], "custom")
        self.assertIn("Ask before installing browser tooling.", plan["environment_notes"])
        self.assertIn("does not discover endpoints", plan["environment_description"])

    def test_artifact_suggestions_follow_validation_preference(self) -> None:
        visual = suggest_artifact_kinds("Improve Blender spatial scene placement", "best_quality")
        efficient = suggest_artifact_kinds("Improve API client retry code", "resource_efficient")
        delegated = suggest_artifact_kinds("Improve planning for research agents", "agent_decides")

        self.assertIn("render", visual)
        self.assertIn("scene_summary", visual)
        self.assertIn("test_output", efficient)
        self.assertIn("structured_summary", efficient)
        self.assertIn("agent_selected_artifacts", delegated)

    def test_unit_id_from_name_is_stable_and_readable(self) -> None:
        self.assertEqual(unit_id_from_name("SVG Quality Harness"), "svg-quality-harness")
        self.assertEqual(unit_id_from_name("  3D / Spatial!!! "), "3d-spatial")
        self.assertEqual(unit_id_from_name(""), "new-harness-unit")

    def test_preferences_can_be_loaded_and_updated_without_touching_user_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)

            preferences = load_preferences(base_dir)
            self.assertEqual(preferences["validation"]["mode"], DEFAULT_PREFERENCES["validation"]["mode"])

            updated = update_preference(base_dir, "validation.mode", "resource_efficient")
            self.assertEqual(updated["validation"]["mode"], "resource_efficient")
            self.assertEqual(load_preferences(base_dir)["validation"]["mode"], "resource_efficient")

    def test_unit_registry_registers_units_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            unit = init_unit(root / "demo-unit", "demo-unit", "Demo Unit")

            record = register_unit(root / "harneloop-home", unit)
            units = list_registered_units(root / "harneloop-home")

            self.assertEqual(record["id"], "demo-unit")
            self.assertEqual(record["name"], "Demo Unit")
            self.assertEqual(len(units), 1)
            self.assertEqual(Path(units[0]["path"]), unit)

    def test_settings_commands_show_and_update_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = str(Path(temp_dir) / "harneloop-home")

            output = StringIO()
            with redirect_stdout(output):
                set_result = main(["settings", "set", "validation.mode", "best_quality", "--home", home])
            output = StringIO()
            with redirect_stdout(output):
                show_result = main(["settings", "show", "--home", home])

            self.assertEqual(set_result, 0)
            self.assertEqual(show_result, 0)
            self.assertIn('"validation"', output.getvalue())
            self.assertIn('"best_quality"', output.getvalue())

    def test_unit_commands_register_and_list_units(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = str(root / "harneloop-home")
            unit = init_unit(root / "demo-unit", "demo-unit", "Demo Unit")

            output = StringIO()
            with redirect_stdout(output):
                register_result = main(["units", "register", str(unit), "--home", home])
            output = StringIO()
            with redirect_stdout(output):
                list_result = main(["units", "list", "--home", home])

            self.assertEqual(register_result, 0)
            self.assertEqual(list_result, 0)
            self.assertIn("Demo Unit", output.getvalue())
            self.assertIn(str(unit), output.getvalue())

    def test_init_unit_registers_unit_unless_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "harneloop-home"

            with redirect_stdout(StringIO()):
                result = main(
                    [
                        "init-unit",
                        str(root / "demo-unit"),
                        "--id",
                        "demo-unit",
                        "--name",
                        "Demo Unit",
                        "--home",
                        str(home),
                    ]
                )

            self.assertEqual(result, 0)
            self.assertEqual([unit["id"] for unit in list_registered_units(home)], ["demo-unit"])

    def test_registered_unit_id_works_outside_unit_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "harneloop-home"
            elsewhere = root / "elsewhere"
            elsewhere.mkdir()
            unit = init_unit(root / "demo-unit", "demo-unit", "Demo Unit")
            connect_environment(
                unit,
                name="Existing environment",
                mode="existing",
                description="A mapped test environment.",
                interaction_mode="custom",
            )
            register_unit(home, unit)

            original_cwd = Path.cwd()
            try:
                os.chdir(elsewhere)
                with patch.dict(os.environ, {"HARNELOOP_HOME": str(home)}):
                    status_output = StringIO()
                    with redirect_stdout(status_output):
                        status_result = main(["status", "demo-unit", "--format", "markdown"])
                    environment_output = StringIO()
                    with redirect_stdout(environment_output):
                        environment_result = main(["environment", "status", "Demo Unit"])
            finally:
                os.chdir(original_cwd)

            self.assertEqual(status_result, 0)
            self.assertEqual(environment_result, 0)
            self.assertIn("Current State", status_output.getvalue())
            self.assertIn("Existing environment", environment_output.getvalue())

    def test_resolve_unit_reference_reports_stale_registry_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "harneloop-home"
            unit = init_unit(root / "demo-unit", "demo-unit", "Demo Unit")
            register_unit(home, unit)
            unit.rename(root / "moved-unit")

            with self.assertRaisesRegex(HarneloopError, "registered path no longer exists"):
                resolve_unit_reference("demo-unit", home)

    def test_candidate_cli_manages_parallel_classified_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            unit = init_unit(Path(temp_dir) / "demo-unit", "demo-unit", "Demo Unit")

            with redirect_stdout(StringIO()):
                first_result = main(
                    [
                        "candidate",
                        "create",
                        str(unit),
                        "--summary",
                        "Accumulate tool improvements",
                        "--plane",
                        "target_harness",
                        "--validation-tier",
                        "representative",
                    ]
                )
                second_result = main(
                    [
                        "candidate",
                        "create",
                        str(unit),
                        "--summary",
                        "Repair the evaluator",
                        "--plane",
                        "evaluation",
                        "--validation-tier",
                        "targeted",
                    ]
                )
                stage_result = main(["candidate", "stage", str(unit), "cand-0002", "ready"])

            output = StringIO()
            with redirect_stdout(output):
                list_result = main(["candidate", "list", str(unit), "--format", "json"])
            records = json.loads(output.getvalue())

            self.assertEqual(first_result, 0)
            self.assertEqual(second_result, 0)
            self.assertEqual(stage_result, 0)
            self.assertEqual(list_result, 0)
            self.assertEqual([record["id"] for record in records], ["cand-0001", "cand-0002"])
            self.assertEqual(records[0]["plane"], "target_harness")
            self.assertEqual(records[1]["status"], "ready")


if __name__ == "__main__":
    unittest.main()
