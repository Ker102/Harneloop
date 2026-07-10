from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import EvoRigError
from .locking import file_lock, harness_lock_path
from .runs import read_run
from .state import now_iso
from .versioning import candidate_root, ensure_unit
from .yamlio import read_yaml, write_yaml


def evidence_root(unit_root: Path, candidate_id: str) -> Path:
    root = candidate_root(unit_root, candidate_id) / "evidence"
    root.mkdir(parents=True, exist_ok=True)
    return root


def next_evidence_id(unit_root: Path, candidate_id: str) -> str:
    root = evidence_root(unit_root, candidate_id)
    existing: list[int] = []
    for path in root.glob("evidence-*.yaml"):
        try:
            existing.append(int(path.stem.removeprefix("evidence-")))
        except ValueError:
            continue
    return f"evidence-{(max(existing, default=0) + 1):04d}"


def list_evidence(unit_root: Path, candidate_id: str) -> list[dict[str, Any]]:
    root = evidence_root(unit_root, candidate_id)
    records = [read_yaml(path) for path in sorted(root.glob("evidence-*.yaml"))]
    return [record for record in records if record]


def validate_evidence_references(unit_root: Path, record: dict[str, Any]) -> None:
    run_id = record.get("run_id")
    artifact_id = record.get("artifact_id")
    evidence_path = record.get("path")

    if artifact_id and not run_id:
        raise EvoRigError(f"Evidence artifact `{artifact_id}` requires a run_id")

    run_record: dict[str, Any] | None = None
    if run_id:
        run_file = unit_root / "runtime" / "runs" / str(run_id) / "run.yaml"
        if not run_file.is_file():
            raise EvoRigError(f"Run does not exist: {run_id}")
        run_record = read_run(unit_root, str(run_id))

    if artifact_id:
        artifacts = (run_record.get("artifacts") or []) if run_record else []
        artifact = next((item for item in artifacts if item.get("id") == artifact_id), None)
        if artifact is None:
            raise EvoRigError(f"Artifact does not exist in run `{run_id}`: {artifact_id}")
        stored_path = artifact.get("stored_path")
        stored_file = (unit_root / str(stored_path)).resolve() if stored_path else None
        if stored_file is None or not stored_file.is_file():
            raise EvoRigError(f"Artifact stored file does not exist for `{artifact_id}` in run `{run_id}`")

    if evidence_path:
        referenced_file = Path(str(evidence_path))
        if not referenced_file.is_absolute():
            referenced_file = unit_root / referenced_file
        if not referenced_file.is_file():
            raise EvoRigError(f"Evidence file does not exist: {referenced_file}")


def add_evidence(
    unit_root: Path,
    candidate_id: str,
    kind: str,
    summary: str,
    outcome: str = "supports",
    run_id: str | None = None,
    artifact_id: str | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    ensure_unit(unit_root)
    if not summary.strip():
        raise EvoRigError("Evidence summary cannot be empty")

    unit_root = unit_root.resolve()
    with file_lock(harness_lock_path(unit_root, f"candidate-{candidate_id}-evidence")):
        evidence_id = next_evidence_id(unit_root, candidate_id)
        resolved_path = path.resolve() if path else None
        record: dict[str, Any] = {
            "id": evidence_id,
            "candidate_id": candidate_id,
            "kind": kind,
            "summary": summary,
            "outcome": outcome,
            "run_id": run_id,
            "artifact_id": artifact_id,
            "path": str(resolved_path) if resolved_path else None,
            "created_at": now_iso(),
        }
        validate_evidence_references(unit_root, record)
        write_yaml(evidence_root(unit_root, candidate_id) / f"{evidence_id}.yaml", record)
        return record


def has_promotion_evidence(unit_root: Path, candidate_id: str) -> bool:
    records = list_evidence(unit_root, candidate_id)
    supporting = [record for record in records if record.get("outcome") in {"supports", "mixed", "neutral"}]
    for record in supporting:
        validate_evidence_references(unit_root.resolve(), record)
    return bool(supporting)
