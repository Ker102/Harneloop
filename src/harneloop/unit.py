from __future__ import annotations

from pathlib import Path

from .errors import HarneloopError
from .operational_map import write_initial_operational_map
from .state import now_iso, write_state
from .templates import apply_template
from .yamlio import write_yaml


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
                "- Create candidate patches before changing promoted harness material.",
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

    write_initial_operational_map(unit_root, unit_id, name)

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
            "reason": "unit_initialized",
            "next_action": "Create a candidate or add initial harness material through the lifecycle.",
        },
    )

    return unit_root
