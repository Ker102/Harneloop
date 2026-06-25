from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .yamlio import write_yaml


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def state_dir(unit_root: Path) -> Path:
    return unit_root / ".evolve"


def state_path(unit_root: Path) -> Path:
    return state_dir(unit_root) / "state.json"


def allowed_edits_path(unit_root: Path) -> Path:
    return state_dir(unit_root) / "allowed-edits.yaml"


def read_state(unit_root: Path) -> dict[str, Any]:
    path = state_path(unit_root)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def write_state(unit_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    state = dict(state)
    state["updated_at"] = now_iso()
    state_dir(unit_root).mkdir(parents=True, exist_ok=True)
    with state_path(unit_root).open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")
    write_state_markdown(unit_root, state)
    write_allowed_edits(unit_root, state)
    return state


def update_state(unit_root: Path, **updates: Any) -> dict[str, Any]:
    state = read_state(unit_root)
    state.update(updates)
    return write_state(unit_root, state)


def write_state_markdown(unit_root: Path, state: dict[str, Any]) -> None:
    current = state_dir(unit_root) / "CURRENT_STATE.md"
    next_action = state_dir(unit_root) / "NEXT_ACTION.md"
    current.write_text(render_state_markdown(state), encoding="utf-8", newline="\n")
    next_action.write_text(render_next_action_markdown(state), encoding="utf-8", newline="\n")


def render_state_markdown(state: dict[str, Any]) -> str:
    lines = [
        "# Current State",
        "",
        f"- State: `{state.get('state', 'unknown')}`",
        f"- Current version: `{state.get('current_version') or 'none'}`",
        f"- Active candidate: `{state.get('active_candidate') or 'none'}`",
        f"- Active run: `{state.get('active_run') or 'none'}`",
        f"- Reason: {state.get('reason') or 'none'}",
        f"- Updated at: `{state.get('updated_at') or 'unknown'}`",
        "",
        "## Next Action",
        "",
        state.get("next_action") or "Inspect the unit state and choose the next lifecycle action.",
    ]
    if state.get("resume_after"):
        lines.append(f"- Resume after: `{state['resume_after']}`")
    if state.get("resume_condition"):
        lines.append(f"- Resume condition: `{state['resume_condition']}`")
    return "\n".join(lines) + "\n"


def render_next_action_markdown(state: dict[str, Any]) -> str:
    next_lines = [
        "# Next Action",
        "",
        state.get("next_action") or "Inspect the unit state and choose the next lifecycle action.",
    ]
    return "\n".join(next_lines) + "\n"


def write_allowed_edits(unit_root: Path, state: dict[str, Any]) -> None:
    active_candidate = state.get("active_candidate")
    allowed_paths = [
        "experiments/**",
        "tools/**",
        "memory/**",
        "agent-facing/drafts/**",
        "observers/drafts/**",
        "validators/drafts/**",
    ]
    if active_candidate:
        allowed_paths.insert(0, f"candidates/{active_candidate}/**")

    write_yaml(
        allowed_edits_path(unit_root),
        {
            "mode": "advisory",
            "active_candidate": active_candidate,
            "allowed_paths": allowed_paths,
            "protected_paths": [
                "unit.yaml",
                "versions/**",
                "provenance/**",
                ".evolve/**",
                "runtime/**",
                "candidates/** except the active candidate path",
            ],
            "notes": [
                "Use framework commands for candidate creation, promotion, rollback, packaging, wait, stop, and resume.",
                "Develop harness changes inside the active candidate before promotion.",
                "Do not edit framework-owned state, promoted versions, provenance, or unit identity by hand.",
            ],
        },
    )


def mark_waiting(
    unit_root: Path,
    reason: str,
    next_action: str,
    resume_after: str | None = None,
    resume_condition: str | None = None,
) -> dict[str, Any]:
    return update_state(
        unit_root,
        state="waiting",
        reason=reason,
        next_action=next_action,
        resume_after=resume_after,
        resume_condition=resume_condition,
    )


def mark_stopped(unit_root: Path, reason: str, next_action: str | None = None) -> dict[str, Any]:
    return update_state(
        unit_root,
        state="stopped",
        reason=reason,
        next_action=next_action or "No automatic next action. Resume only when the reason is resolved.",
    )


def mark_active(unit_root: Path, reason: str | None = None, next_action: str | None = None) -> dict[str, Any]:
    return update_state(
        unit_root,
        state="active",
        reason=reason,
        next_action=next_action or "Continue the current harness lifecycle.",
        resume_after=None,
        resume_condition=None,
    )
