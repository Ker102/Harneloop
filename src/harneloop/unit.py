from __future__ import annotations

from pathlib import Path

from .errors import HarneloopError
from .intake import initialize_intake
from .operational_map import write_initial_operational_map
from .state import now_iso, read_state, write_state
from .templates import apply_template
from .yamlio import read_yaml, write_yaml


RECOMMENDED_DIRS = [
    "candidates",
    "versions",
    "provenance",
    "agent-facing",
    "observers",
    "validators",
    "regression-cases",
    "infrastructure",
    "exports",
    "tools",
    "memory",
    "experiments",
    "attempts",
    "target",
    "environment",
    "runtime/artifacts",
]


def render_unit_agents(name: str) -> str:
    return (
        "\n".join(
            [
                f"# Harneloop Unit: {name}",
                "",
                "When work concerns this harness unit, treat the target task as the test surface for improving the harness, not as permission to forget the Harneloop lifecycle.",
                "",
                "Before substantial unit work or after context loss, read:",
                "",
                "1. `.evolve/SESSION_BRIEF.md`",
                "2. `UNIT_AGENT.md`",
                "3. `operational-map.md`",
                "",
                "Finish every run by evaluating its artifacts and recording an explicit attempt conclusion. A good first result may be accepted with no candidate; incomplete evidence should lead to a rerun or concrete request for input.",
                "Treat candidates as coherent change batches. Several independent candidates may remain open; use `harneloop candidate list <unit>` to recover them and scale validation to each candidate's impact.",
                "",
                "These instructions are scoped to work involving this harness unit. Other project work in the same conversation remains outside this unit unless explicitly connected.",
            ]
        )
        + "\n"
    )


def upgrade_unit_protocol(unit_root: Path) -> list[str]:
    unit_root = unit_root.resolve()
    unit_path = unit_root / "unit.yaml"
    if not unit_path.exists():
        raise HarneloopError(f"Not a Harneloop harness unit: {unit_root}")
    unit = read_yaml(unit_path)
    created: list[str] = []
    agents_path = unit_root / "AGENTS.md"
    if not agents_path.exists():
        agents_path.write_text(render_unit_agents(str(unit.get("name") or unit.get("id"))), encoding="utf-8", newline="\n")
        created.append("AGENTS.md")
    intake = unit_root / ".evolve" / "intake.yaml"
    if not intake.exists():
        initialize_intake(unit_root)
        created.append(".evolve/intake.yaml")
    brief = unit_root / ".evolve" / "SESSION_BRIEF.md"
    if not brief.exists():
        write_state(unit_root, read_state(unit_root))
        created.append(".evolve/SESSION_BRIEF.md")
    return created


def init_unit(path: Path, unit_id: str, name: str, template: str = "blank") -> Path:
    unit_root = path.resolve()
    if unit_root.exists() and any(unit_root.iterdir()):
        raise HarneloopError(f"Harness unit path is not empty: {unit_root}")

    unit_root.mkdir(parents=True, exist_ok=True)
    for directory in RECOMMENDED_DIRS:
        (unit_root / directory).mkdir(parents=True, exist_ok=True)

    write_yaml(
        unit_root / "unit.yaml",
        {
            "schema_version": "0.1",
            "id": unit_id,
            "name": name,
            "product_name": "Harneloop",
            "name_status": "selected",
            "template": template,
            "created_at": now_iso(),
            "current_version": None,
        },
    )

    (unit_root / "UNIT_AGENT.md").write_text(
        "\n".join(
            [
                f"# {name}",
                "",
                "This harness unit is an agent sandbox with a strict lifecycle.",
                "Use `operational-map.md` as the current orientation for how this unit is tested, what evidence matters, and what the agent currently believes about the environment.",
                "Update the map when the workflow, artifact paths, evidence needs, environment assumptions, or automation strategy change.",
                "",
                "Rules:",
                "",
                "- Read `operational-map.md` before planning the first baseline attempt.",
                "- Create or extend a coherent candidate before changing promoted harness material; do not create one candidate per edit.",
                "- Keep independent target-harness, evaluation, and infrastructure changes in separate candidates when practical.",
                "- Scale validation to impact: structural, targeted, representative, or full.",
                "- Put exploratory work inside candidate, experiment, tool, memory, or research folders.",
                "- Do not edit framework-owned state, promoted versions, or provenance by hand.",
                "- Promotion must go through the Harneloop engine.",
                "- Stop and wait states are normal lifecycle outcomes when evidence, time, or permissions require it.",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    (unit_root / "AGENTS.md").write_text(render_unit_agents(name), encoding="utf-8", newline="\n")

    write_initial_operational_map(unit_root, unit_id, name)
    initialize_intake(unit_root)

    (unit_root / "provenance" / "changelog.md").write_text(
        f"# Changelog\n\n- {now_iso()}: Created harness unit `{unit_id}`.\n",
        encoding="utf-8",
        newline="\n",
    )

    apply_template(unit_root, template)

    write_state(
        unit_root,
        {
            "state": "active",
            "unit_id": unit_id,
            "current_version": None,
            "active_candidate": None,
            "active_candidates": [],
            "reason": "unit_initialized",
            "next_action": "Create a candidate or add initial harness material through the lifecycle.",
        },
    )

    return unit_root
