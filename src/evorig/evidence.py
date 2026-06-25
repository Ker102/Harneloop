from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import EvoRigError
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

    evidence_id = next_evidence_id(unit_root, candidate_id)
    record: dict[str, Any] = {
        "id": evidence_id,
        "candidate_id": candidate_id,
        "kind": kind,
        "summary": summary,
        "outcome": outcome,
        "run_id": run_id,
        "artifact_id": artifact_id,
        "path": str(path) if path else None,
        "created_at": now_iso(),
    }
    write_yaml(evidence_root(unit_root, candidate_id) / f"{evidence_id}.yaml", record)
    return record


def has_promotion_evidence(unit_root: Path, candidate_id: str) -> bool:
    records = list_evidence(unit_root, candidate_id)
    return any(record.get("outcome") in {"supports", "mixed", "neutral"} for record in records)
