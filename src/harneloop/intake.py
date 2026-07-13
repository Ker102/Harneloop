from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import HarneloopError
from .locking import file_lock, harness_lock_path
from .state import now_iso, update_state
from .yamlio import read_yaml, write_yaml


INTAKE_FIELDS: dict[str, str] = {
    "harness_goal": "What should this harness help an agent get better at?",
    "usage_context": "Where will this harness be used?",
    "success_strategy": "Should the user define success, delegate it, or decide after a baseline?",
    "validation_preference": "How should results be validated for this task?",
    "environment_status": "Which target environment and inputs should this harness use?",
}
FIELD_STATUSES = {"confirmed", "user_delegated", "inferred", "unknown", "not_applicable"}
ACKNOWLEDGEMENT_BASES = {"user_confirmed", "user_delegated"}


def intake_path(unit_root: Path) -> Path:
    return unit_root / ".evolve" / "intake.yaml"


def initial_intake() -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "policy": "adaptive",
        "status": "pending",
        "fields": {
            field: {"value": None, "status": "unknown", "source": None, "updated_at": None}
            for field in INTAKE_FIELDS
        },
        "acknowledgement": None,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


def initialize_intake(unit_root: Path) -> dict[str, Any]:
    data = initial_intake()
    write_yaml(intake_path(unit_root), data)
    return data


def read_intake(unit_root: Path) -> dict[str, Any]:
    path = intake_path(unit_root)
    if not path.exists():
        raise HarneloopError("Harness unit has no intake record")
    return read_yaml(path)


def write_intake(unit_root: Path, data: dict[str, Any]) -> dict[str, Any]:
    data = dict(data)
    data["updated_at"] = now_iso()
    write_yaml(intake_path(unit_root), data)
    return data


def resolve_intake_field(
    unit_root: Path,
    field: str,
    *,
    value: str,
    status: str,
    source: str,
) -> dict[str, Any]:
    if field not in INTAKE_FIELDS:
        raise HarneloopError(f"Unknown intake field: {field}")
    if status not in FIELD_STATUSES - {"unknown"}:
        allowed = ", ".join(sorted(FIELD_STATUSES - {"unknown"}))
        raise HarneloopError(f"Invalid intake status `{status}`. Expected one of: {allowed}")
    if not value.strip() and status != "not_applicable":
        raise HarneloopError("Intake field value cannot be empty")
    if not source.strip():
        raise HarneloopError("Intake field source cannot be empty")

    unit_root = unit_root.resolve()
    with file_lock(harness_lock_path(unit_root, "intake")):
        data = read_intake(unit_root)
        data["fields"][field] = {
            "value": value.strip() or None,
            "status": status,
            "source": source.strip(),
            "updated_at": now_iso(),
        }
        data["status"] = "pending"
        data["acknowledgement"] = None
        return write_intake(unit_root, data)


def acknowledge_intake(unit_root: Path, *, basis: str, note: str) -> dict[str, Any]:
    if basis not in ACKNOWLEDGEMENT_BASES:
        allowed = ", ".join(sorted(ACKNOWLEDGEMENT_BASES))
        raise HarneloopError(f"Invalid acknowledgement basis `{basis}`. Expected one of: {allowed}")
    if not note.strip():
        raise HarneloopError("Intake acknowledgement note cannot be empty")

    unit_root = unit_root.resolve()
    with file_lock(harness_lock_path(unit_root, "intake")):
        data = read_intake(unit_root)
        data["status"] = "ready"
        data["acknowledgement"] = {"basis": basis, "note": note.strip(), "at": now_iso()}
        result = write_intake(unit_root, data)
    update_state(
        unit_root,
        reason="intake_acknowledged",
        next_action="Complete the target and environment mapping, then plan the first baseline attempt.",
    )
    return result


def ensure_intake_ready(unit_root: Path) -> None:
    data = read_intake(unit_root)
    if data.get("status") != "ready":
        raise HarneloopError(
            "The adaptive intake checkpoint is still pending. Surface the relevant questions, "
            "then use `harneloop intake resolve` and `harneloop intake acknowledge` before the first run."
        )


def unresolved_intake_fields(data: dict[str, Any]) -> list[str]:
    return [
        field
        for field, record in (data.get("fields") or {}).items()
        if record.get("status") in {"unknown", "inferred"}
    ]


def render_intake_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Adaptive Intake Checkpoint",
        "",
        f"- Status: `{data.get('status', 'pending')}`",
        f"- Policy: `{data.get('policy', 'adaptive')}`",
        "",
        "Inspect first, then ask only the questions that still matter. Do not silently convert inferred context into confirmed unit truth.",
        "",
        "## Context",
        "",
    ]
    fields = data.get("fields") or {}
    for field, question in INTAKE_FIELDS.items():
        record = fields.get(field) or {}
        lines.append(f"- `{field}`: `{record.get('status', 'unknown')}` - {record.get('value') or question}")
        if record.get("source"):
            lines.append(f"  Source: {record['source']}")
    unresolved = unresolved_intake_fields(data)
    lines.extend(["", "## Relevant Follow-Up", ""])
    if unresolved:
        lines.extend(f"- {INTAKE_FIELDS[field]}" for field in unresolved)
    else:
        lines.append("- No unresolved context fields.")
    lines.extend(
        [
            "",
            "Scaffolding and inspection may continue while intake is pending. Before the first real run, record user confirmation or explicit delegation.",
            "",
        ]
    )
    return "\n".join(lines)
