from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import EvoRigError
from .state import now_iso, update_state
from .versioning import ensure_unit
from .yamlio import read_yaml, write_yaml


ENVIRONMENT_MODES = {"existing", "assisted", "managed"}


def normalize_notes(notes: list[str] | tuple[str, ...] | None) -> list[str]:
    return [note for note in (notes or []) if note]


def environment_root(unit_root: Path) -> Path:
    return unit_root / "environment"


def contract_path(unit_root: Path) -> Path:
    return environment_root(unit_root) / "contract.yaml"


def connect_environment(
    unit_root: Path,
    name: str,
    mode: str,
    description: str,
    run_command: str | None = None,
    artifact_path: str | None = None,
    notes: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    ensure_unit(unit_root)
    if mode not in ENVIRONMENT_MODES:
        supported = ", ".join(sorted(ENVIRONMENT_MODES))
        raise EvoRigError(f"Unknown environment mode `{mode}`. Expected one of: {supported}")

    root = environment_root(unit_root)
    root.mkdir(parents=True, exist_ok=True)
    contract: dict[str, Any] = {
        "schema_version": "0.1",
        "name": name,
        "mode": mode,
        "description": description,
        "run_command": run_command,
        "artifact_path": artifact_path,
        "notes": normalize_notes(notes),
        "created_at": now_iso(),
    }
    write_yaml(contract_path(unit_root), contract)
    (root / "README.md").write_text(render_environment_status(unit_root, contract), encoding="utf-8", newline="\n")
    update_state(
        unit_root,
        reason="environment_connected",
        next_action="Run a baseline task and capture artifacts through the declared environment contract.",
    )
    return contract


def read_environment_contract(unit_root: Path) -> dict[str, Any]:
    path = contract_path(unit_root)
    if not path.exists():
        raise EvoRigError("No environment contract exists. Run `evorig environment connect` first.")
    return read_yaml(path)


def render_environment_status(unit_root: Path, contract: dict[str, Any] | None = None) -> str:
    data = contract or read_environment_contract(unit_root)
    mode = data.get("mode")
    if mode == "existing":
        mode_guidance = "Connect to the existing environment. Do not rebuild it unless checks fail or the user asks."
    elif mode == "assisted":
        mode_guidance = "Assist setup by proposing missing commands, dependencies, or artifact capture steps."
    else:
        mode_guidance = "Managed setup is allowed, but every infrastructure change should be explicit."

    lines = [
        "# Environment Contract",
        "",
        f"- Name: {data.get('name')}",
        f"- Mode: `{mode}`",
        f"- Description: {data.get('description')}",
        f"- Run command: `{data.get('run_command') or 'not declared'}`",
        f"- Artifact path: `{data.get('artifact_path') or 'not declared'}`",
        "",
        "## Mode Guidance",
        "",
        mode_guidance,
    ]
    notes = data.get("notes") or []
    if notes:
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in notes)
    return "\n".join(lines) + "\n"
