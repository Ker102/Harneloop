from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .locking import file_lock, harness_lock_path
from .yamlio import write_yaml
from .yamlio import read_yaml


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
    temp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            dir=state_dir(unit_root),
            prefix=".state.json.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = handle.name
            json.dump(state, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, state_path(unit_root))
    finally:
        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink()
    write_state_markdown(unit_root, state)
    write_allowed_edits(unit_root, state)
    return state


def update_state(unit_root: Path, **updates: Any) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    with file_lock(harness_lock_path(unit_root, "state")):
        state = read_state(unit_root)
        state.update(updates)
        return write_state(unit_root, state)


def write_state_markdown(unit_root: Path, state: dict[str, Any]) -> None:
    current = state_dir(unit_root) / "CURRENT_STATE.md"
    next_action = state_dir(unit_root) / "NEXT_ACTION.md"
    current.write_text(render_state_markdown(state), encoding="utf-8", newline="\n")
    next_action.write_text(render_next_action_markdown(state), encoding="utf-8", newline="\n")
    (state_dir(unit_root) / "SESSION_BRIEF.md").write_text(
        render_session_brief_markdown(build_session_brief_data(unit_root, state)),
        encoding="utf-8",
        newline="\n",
    )


def _read_optional_yaml(path: Path) -> dict[str, Any]:
    return read_yaml(path) if path.exists() else {}


def _latest_attempt(unit_root: Path) -> dict[str, Any]:
    attempts_root = unit_root / "attempts"
    if not attempts_root.exists():
        return {}
    for attempt_root in sorted(attempts_root.glob("attempt-*"), reverse=True):
        attempt = _read_optional_yaml(attempt_root / "attempt.yaml")
        if attempt:
            return attempt
    return {}


def _active_candidate_ids(state: dict[str, Any]) -> list[str]:
    active = state.get("active_candidates")
    if isinstance(active, list):
        return [str(candidate_id) for candidate_id in active if candidate_id]
    focused = state.get("active_candidate")
    return [str(focused)] if focused else []


def _candidate_summaries(unit_root: Path, candidate_ids: list[str]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for candidate_id in candidate_ids:
        record = _read_optional_yaml(unit_root / "candidates" / candidate_id / "candidate.yaml")
        if record:
            summaries.append(
                {
                    "id": candidate_id,
                    "summary": record.get("summary"),
                    "status": record.get("status", "draft"),
                    "plane": record.get("plane", record.get("kind", "legacy")),
                    "validation_tier": record.get("validation_tier", "legacy"),
                }
            )
    return summaries


def build_session_brief_data(unit_root: Path, state: dict[str, Any] | None = None) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    unit = _read_optional_yaml(unit_root / "unit.yaml")
    target = _read_optional_yaml(unit_root / "target" / "brief.yaml")
    intake = _read_optional_yaml(unit_root / ".evolve" / "intake.yaml")
    current_state = state or read_state(unit_root)
    latest_attempt = _latest_attempt(unit_root)
    conclusions = latest_attempt.get("conclusions") or []
    unresolved = [
        field
        for field, record in (intake.get("fields") or {}).items()
        if record.get("status") in {"unknown", "inferred"}
    ]
    return {
        "scope": "When working on this unit, use Harneloop to improve the harness; unrelated work in the same agent session is outside this brief.",
        "unit_id": unit.get("id") or current_state.get("unit_id"),
        "unit_name": unit.get("name") or "Unknown harness unit",
        "target_task": target.get("task") or latest_attempt.get("goal"),
        "success": target.get("success"),
        "state": current_state.get("state", "unknown"),
        "current_version": current_state.get("current_version"),
        "active_candidate": current_state.get("active_candidate"),
        "active_candidates": _candidate_summaries(unit_root, _active_candidate_ids(current_state)),
        "active_run": current_state.get("active_run"),
        "intake_status": intake.get("status", "missing"),
        "unresolved_intake": unresolved,
        "latest_conclusion": conclusions[-1] if conclusions else None,
        "next_action": current_state.get("next_action"),
        "updated_at": current_state.get("updated_at"),
    }


def render_session_brief_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Harneloop Unit Brief",
        "",
        data["scope"],
        "",
        f"- Harness unit: `{data.get('unit_name')}` (`{data.get('unit_id')}`)",
        f"- Target: {data.get('target_task') or 'not mapped yet'}",
        f"- State: `{data.get('state')}`",
        f"- Intake: `{data.get('intake_status')}`",
        f"- Current version: `{data.get('current_version') or 'none'}`",
        f"- Focused candidate: `{data.get('active_candidate') or 'none'}`",
        f"- Active run: `{data.get('active_run') or 'none'}`",
    ]
    active_candidates = data.get("active_candidates") or []
    if active_candidates:
        lines.extend(["", "## Open Candidates", ""])
        for candidate in active_candidates:
            lines.append(
                f"- `{candidate.get('id')}`: `{candidate.get('status')}` / `{candidate.get('plane')}` / "
                f"`{candidate.get('validation_tier')}` - {candidate.get('summary') or 'no summary'}"
            )
    unresolved = data.get("unresolved_intake") or []
    if unresolved:
        lines.append(f"- Unresolved or inferred context: `{', '.join(unresolved)}`")
    conclusion = data.get("latest_conclusion")
    if conclusion:
        lines.extend(
            [
                "",
                "## Latest Evaluation Decision",
                "",
                f"- Outcome: `{conclusion.get('outcome')}`",
                f"- Decision: `{conclusion.get('decision')}`",
                f"- Confidence: `{conclusion.get('confidence')}`",
                f"- Summary: {conclusion.get('summary')}",
            ]
        )
    lines.extend(["", "## Next Action", "", data.get("next_action") or "Inspect the unit and choose the next lifecycle action.", ""])
    return "\n".join(lines)


def render_state_markdown(state: dict[str, Any]) -> str:
    lines = [
        "# Current State",
        "",
        f"- State: `{state.get('state', 'unknown')}`",
        f"- Current version: `{state.get('current_version') or 'none'}`",
        f"- Focused candidate: `{state.get('active_candidate') or 'none'}`",
        f"- Open candidates: `{', '.join(_active_candidate_ids(state)) or 'none'}`",
        f"- Active run: `{state.get('active_run') or 'none'}`",
        f"- Reason: {state.get('reason') or 'none'}",
        f"- Updated at: `{state.get('updated_at') or 'unknown'}`",
        "",
        "## Next Action",
        "",
        state.get("next_action") or "Inspect the harness unit state and choose the next lifecycle action.",
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
        state.get("next_action") or "Inspect the harness unit state and choose the next lifecycle action.",
    ]
    return "\n".join(next_lines) + "\n"


def write_allowed_edits(unit_root: Path, state: dict[str, Any]) -> None:
    active_candidates = _active_candidate_ids(state)
    allowed_paths = [
        "experiments/**",
        "tools/**",
        "memory/**",
        "agent-facing/drafts/**",
        "observers/drafts/**",
        "validators/drafts/**",
    ]
    for candidate_id in reversed(active_candidates):
        allowed_paths.insert(0, f"candidates/{candidate_id}/**")

    write_yaml(
        allowed_edits_path(unit_root),
        {
            "mode": "advisory",
            "active_candidate": state.get("active_candidate"),
            "active_candidates": active_candidates,
            "allowed_paths": allowed_paths,
            "protected_paths": [
                "unit.yaml",
                "versions/**",
                "provenance/**",
                ".evolve/**",
                "runtime/**",
                "candidates/** except open candidate paths",
            ],
            "notes": [
                "Use framework commands for candidate creation, promotion, rollback, packaging, wait, stop, and resume.",
                "Develop each coherent harness change batch inside an open candidate before promotion.",
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
