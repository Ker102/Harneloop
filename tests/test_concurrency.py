from __future__ import annotations

import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from harneloop.preferences import list_registered_units, register_unit
from harneloop.runs import add_artifact, read_run, start_run
from harneloop.intake import acknowledge_intake
from harneloop.unit import init_unit


class ConcurrencyTests(unittest.TestCase):
    def test_parallel_unit_registrations_do_not_lose_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "harneloop-home"
            units = [init_unit(root / f"unit-{index}", f"unit-{index}", f"Unit {index}") for index in range(12)]
            start = threading.Event()

            def worker(unit: Path) -> str:
                start.wait(timeout=5)
                return str(register_unit(home, unit)["id"])

            with ThreadPoolExecutor(max_workers=len(units)) as executor:
                futures = [executor.submit(worker, unit) for unit in units]
                start.set()
                returned_ids = [future.result(timeout=10) for future in futures]

            registered_ids = [str(record["id"]) for record in list_registered_units(home)]
            self.assertEqual(len(registered_ids), len(units))
            self.assertEqual(set(registered_ids), set(returned_ids))

    def test_parallel_artifact_adds_do_not_lose_run_yaml_updates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            harness_unit = init_unit(root / "unit", "demo", "Demo Unit")
            acknowledge_intake(harness_unit, basis="user_delegated", note="Test delegates setup context.")
            start_run(harness_unit, task="Capture artifacts concurrently")

            sources = []
            for index in range(12):
                source = root / f"artifact-{index}.txt"
                source.write_text(f"artifact {index}\n", encoding="utf-8")
                sources.append(source)

            start = threading.Event()

            def worker(source: Path) -> str:
                start.wait(timeout=5)
                record = add_artifact(
                    harness_unit,
                    "run-0001",
                    source,
                    kind="text",
                    description=source.name,
                )
                return str(record["id"])

            with ThreadPoolExecutor(max_workers=len(sources)) as executor:
                futures = [executor.submit(worker, source) for source in sources]
                start.set()
                returned_ids = [future.result(timeout=10) for future in futures]

            run_record = read_run(harness_unit, "run-0001")
            stored_artifacts = run_record["artifacts"]
            stored_ids = [artifact["id"] for artifact in stored_artifacts]

            self.assertEqual(len(stored_artifacts), len(sources))
            self.assertEqual(len(set(stored_ids)), len(sources))
            self.assertEqual(len(set(returned_ids)), len(sources))


if __name__ == "__main__":
    unittest.main()
