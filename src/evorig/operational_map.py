from __future__ import annotations

from pathlib import Path


OPERATIONAL_MAP_FILENAME = "operational-map.md"


def render_operational_map(unit_id: str, name: str) -> str:
    return "\n".join(
        [
            "# Current Operational Map",
            "",
            f"Harness unit: `{name}` (`{unit_id}`)",
            "",
            "Use this map as current orientation. Update it when the harness unit's workflow, evidence needs, or environment assumptions change. The agent should still reason from the task, inspect available evidence, and choose the most appropriate test/evaluation strategy.",
            "",
            "This is context and navigation, not a rigid procedure.",
            "",
            "## What This Harness Unit Is Trying To Improve",
            "",
            "- Current understanding:",
            "- What better may mean right now:",
            "- Open questions:",
            "",
            "## Systems, Tools, And Environment",
            "",
            "- Systems and tools it interacts with:",
            "- Environment entry points:",
            "- Reset or restart notes:",
            "- What EvoRig records:",
            "  - `target/brief.yaml`",
            "  - `environment/contract.yaml`",
            "  - `attempts/`",
            "  - `runtime/runs/`",
            "  - `runtime/artifacts/`",
            "",
            "EvoRig records mappings, but the onboarding agent must inspect the real workspace, tools, commands, endpoints, and artifact paths.",
            "",
            "## Useful Artifacts And Evidence",
            "",
            "- Currently useful artifacts:",
            "- Where artifacts usually appear before capture:",
            "- Useful structured summaries, logs, screenshots, renders, traces, or review notes:",
            "- How evidence is usually attached:",
            "  - `evorig artifact add ...`",
            "  - `evorig attempt observe ...`",
            "  - `evorig candidate evidence add ...`",
            "",
            "Choose artifacts and evidence from the current task and observed result, not from habit.",
            "",
            "## Running And Resetting The Environment",
            "",
            "- Usual run path:",
            "- Usual reset path:",
            "- Manual steps still required:",
            "- Automation opportunities:",
            "",
            "## Automation And Autonomy",
            "",
            "The agent should aim to run repeated testing/improvement loops without requiring the user to manually restart apps, reinstall addons, reset services, or collect files.",
            "",
            "If automating the environment is reasonable, implement or document that automation.",
            "",
            "If automation is risky, unclear, or too expensive/time-consuming, ask the user before proceeding.",
            "",
            "## Known Constraints, Fragile Spots, And Open Questions",
            "",
            "- Constraints:",
            "- Fragile spots:",
            "- Open questions:",
            "",
            "## Current Assumptions To Re-Check",
            "",
            "- Assumptions:",
            "",
            "## Prior Runs, Evidence, And Decisions",
            "",
            "- Runs: `runtime/runs/`",
            "- Artifacts: `runtime/artifacts/`",
            "- Attempt plans and observations: `attempts/`",
            "- Candidate evidence: `candidates/*/evidence/`",
            "- Promotion history: `provenance/changelog.md`",
            "",
        ]
    )


def write_initial_operational_map(unit_root: Path, unit_id: str, name: str) -> Path:
    path = unit_root / OPERATIONAL_MAP_FILENAME
    path.write_text(render_operational_map(unit_id, name), encoding="utf-8", newline="\n")
    return path
