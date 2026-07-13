from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import HarneloopError
from .locking import file_lock, harness_lock_path
from .runs import read_run, write_run
from .state import now_iso, update_state
from .versioning import ensure_unit
from .yamlio import read_yaml, write_yaml


def normalize_list(value: list[str] | tuple[str, ...] | None) -> list[str]:
    return [item for item in (value or []) if item]


def attempts_root(unit_root: Path) -> Path:
    return unit_root / "attempts"


def next_attempt_id(unit_root: Path) -> str:
    root = attempts_root(unit_root)
    root.mkdir(parents=True, exist_ok=True)
    existing: list[int] = []
    for path in root.iterdir():
        if path.is_dir() and path.name.startswith("attempt-"):
            try:
                existing.append(int(path.name.removeprefix("attempt-")))
            except ValueError:
                continue
    return f"attempt-{(max(existing, default=0) + 1):04d}"


def attempt_path(unit_root: Path, attempt_id: str) -> Path:
    path = attempts_root(unit_root) / attempt_id
    if not path.exists():
        raise HarneloopError(f"Attempt plan does not exist: {attempt_id}")
    return path


def read_attempt(unit_root: Path, attempt_id: str) -> dict[str, Any]:
    return read_yaml(attempt_path(unit_root, attempt_id) / "attempt.yaml")


def write_attempt(unit_root: Path, attempt_id: str, data: dict[str, Any]) -> dict[str, Any]:
    write_yaml(attempt_path(unit_root, attempt_id) / "attempt.yaml", data)
    write_observations_markdown(unit_root, attempt_id, data)
    return data


def create_attempt_plan(
    unit_root: Path,
    goal: str,
    method: str,
    action: list[str] | tuple[str, ...] | None = None,
    expected_artifact: list[str] | tuple[str, ...] | None = None,
    success_check: list[str] | tuple[str, ...] | None = None,
    note: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    ensure_unit(unit_root)
    if not goal.strip():
        raise HarneloopError("Attempt goal cannot be empty")
    if not method.strip():
        raise HarneloopError("Attempt method cannot be empty")

    with file_lock(harness_lock_path(unit_root, "attempts")):
        attempt_id = next_attempt_id(unit_root)
        root = attempts_root(unit_root) / attempt_id
        root.mkdir(parents=True, exist_ok=False)
        data: dict[str, Any] = {
            "schema_version": "0.1",
            "id": attempt_id,
            "goal": goal,
            "method": method,
            "actions": normalize_list(action),
            "expected_artifacts": normalize_list(expected_artifact),
            "success_checks": normalize_list(success_check),
            "notes": normalize_list(note),
            "observations": [],
            "conclusions": [],
            "created_at": now_iso(),
        }
        write_attempt(unit_root, attempt_id, data)
    update_state(
        unit_root,
        reason="attempt_plan_created",
        next_action=f"Execute `{attempt_id}` with the target agent/tools, then start a run and capture artifacts.",
    )
    return data


def add_attempt_observation(
    unit_root: Path,
    attempt_id: str,
    summary: str,
    outcome: str = "unknown",
    run_id: str | None = None,
    finding: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    if not summary.strip():
        raise HarneloopError("Observation summary cannot be empty")
    unit_root = unit_root.resolve()
    with file_lock(harness_lock_path(unit_root, f"attempt-{attempt_id}")):
        data = read_attempt(unit_root, attempt_id)
        observations = data.get("observations") or []
        observation = {
            "id": f"observation-{len(observations) + 1:04d}",
            "summary": summary,
            "outcome": outcome,
            "run_id": run_id,
            "findings": normalize_list(finding),
            "created_at": now_iso(),
        }
        data["observations"] = [*observations, observation]
        write_attempt(unit_root, attempt_id, data)
    update_state(
        unit_root,
        reason="attempt_observation_added",
        next_action="Use observations to create evidence, candidate changes, or another attempt plan.",
    )
    return observation


VALID_CONCLUSION_OUTCOMES = {"pass", "partial", "fail", "inconclusive"}
VALID_CONCLUSION_DECISIONS = {"accept", "create_candidate", "rerun", "request_input", "stop"}
VALID_CONFIDENCE = {"low", "medium", "high"}


def conclude_attempt(
    unit_root: Path,
    attempt_id: str,
    *,
    run_id: str,
    outcome: str,
    decision: str,
    summary: str,
    confidence: str,
    question: str | None = None,
) -> dict[str, Any]:
    if outcome not in VALID_CONCLUSION_OUTCOMES:
        raise HarneloopError(f"Invalid attempt outcome: {outcome}")
    if decision not in VALID_CONCLUSION_DECISIONS:
        raise HarneloopError(f"Invalid attempt decision: {decision}")
    if confidence not in VALID_CONFIDENCE:
        raise HarneloopError(f"Invalid conclusion confidence: {confidence}")
    if not summary.strip():
        raise HarneloopError("Attempt conclusion summary cannot be empty")
    if decision == "request_input" and not (question or "").strip():
        raise HarneloopError("The `request_input` decision requires a concrete question")
    if decision == "accept" and outcome != "pass":
        raise HarneloopError("Only a passing attempt can be accepted without further work")

    unit_root = unit_root.resolve()
    run = read_run(unit_root, run_id)
    if run.get("status") == "running":
        raise HarneloopError(f"Run must be finished before evaluation: {run_id}")
    if run.get("attempt_id") != attempt_id:
        raise HarneloopError(f"Run `{run_id}` is not linked to attempt `{attempt_id}`")

    with file_lock(harness_lock_path(unit_root, f"attempt-{attempt_id}")):
        data = read_attempt(unit_root, attempt_id)
        expected = data.get("expected_artifacts") or []
        captured = {artifact.get("kind") for artifact in (run.get("artifacts") or [])}
        missing = [kind for kind in expected if kind not in captured]
        if outcome == "pass" and missing:
            missing_text = ", ".join(missing)
            raise HarneloopError(f"Passing conclusion is missing expected artifacts: {missing_text}")

        conclusions = data.get("conclusions") or []
        conclusion = {
            "id": f"conclusion-{len(conclusions) + 1:04d}",
            "run_id": run_id,
            "outcome": outcome,
            "decision": decision,
            "summary": summary.strip(),
            "confidence": confidence,
            "captured_artifact_kinds": sorted(kind for kind in captured if kind),
            "missing_expected_artifacts": missing,
            "question": (question or "").strip() or None,
            "created_at": now_iso(),
        }
        data["conclusions"] = [*conclusions, conclusion]
        write_attempt(unit_root, attempt_id, data)

    run["evaluation_status"] = "completed"
    run["evaluation_outcome"] = outcome
    write_run(unit_root, run_id, run)

    if decision == "accept":
        update_state(
            unit_root,
            state="satisfied",
            reason="current_harness_accepted",
            next_action="No candidate is needed for the current evidence. Resume only for broader tests or a changed goal.",
        )
    elif decision == "create_candidate":
        update_state(
            unit_root,
            state="active",
            reason="candidate_change_needed",
            next_action=f"Create a candidate from conclusion `{conclusion['id']}` and retest it.",
        )
    elif decision == "rerun":
        update_state(
            unit_root,
            state="active",
            reason="attempt_rerun_needed",
            next_action="Revise the attempt or evidence plan and run it again before changing the harness.",
        )
    elif decision == "request_input":
        update_state(
            unit_root,
            state="waiting",
            reason="user_input_required",
            next_action=question.strip(),
            resume_condition="The user provides or delegates the requested context or evidence.",
        )
    else:
        update_state(
            unit_root,
            state="stopped",
            reason="attempt_conclusion_stopped",
            next_action="Resume only when the documented stopping reason changes.",
        )
    return conclusion


def write_observations_markdown(unit_root: Path, attempt_id: str, data: dict[str, Any]) -> None:
    lines = [
        f"# Observations For {attempt_id}",
        "",
        f"Goal: {data.get('goal')}",
        "",
    ]
    observations = data.get("observations") or []
    if not observations:
        lines.append("No observations recorded yet.")
    for observation in observations:
        lines.extend(
            [
                f"## {observation.get('id')}",
                "",
                f"- Outcome: `{observation.get('outcome')}`",
                f"- Run: `{observation.get('run_id') or 'none'}`",
                f"- Summary: {observation.get('summary')}",
            ]
        )
        findings = observation.get("findings") or []
        if findings:
            lines.extend(["", "Findings:"])
            lines.extend(f"- {item}" for item in findings)
        lines.append("")
    (attempt_path(unit_root, attempt_id) / "OBSERVATIONS.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
        newline="\n",
    )
