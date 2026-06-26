from __future__ import annotations

from pathlib import Path

from .errors import EvoRigError
from .locking import file_lock, harness_lock_path
from .state import now_iso, update_state
from .yamlio import read_yaml, write_yaml


def next_candidate_id(unit_root: Path) -> str:
    candidates_root = unit_root / "candidates"
    candidates_root.mkdir(parents=True, exist_ok=True)
    existing = []
    for path in candidates_root.iterdir():
        if path.is_dir() and path.name.startswith("cand-"):
            try:
                existing.append(int(path.name.removeprefix("cand-")))
            except ValueError:
                continue
    return f"cand-{(max(existing, default=0) + 1):04d}"


def create_candidate(unit_root: Path, summary: str, kind: str = "mixed") -> Path:
    unit_root = unit_root.resolve()
    if not (unit_root / "unit.yaml").exists():
        raise EvoRigError(f"Not an EvoRig harness unit: {unit_root}")

    with file_lock(harness_lock_path(unit_root, "candidates")):
        candidate_id = next_candidate_id(unit_root)
        candidate_root = unit_root / "candidates" / candidate_id
        candidate_root.mkdir(parents=True, exist_ok=False)
        for directory in ["changes", "validation", "evidence"]:
            (candidate_root / directory).mkdir(parents=True, exist_ok=True)

        unit_meta = read_yaml(unit_root / "unit.yaml")
        write_yaml(
            candidate_root / "candidate.yaml",
            {
                "id": candidate_id,
                "base_version": unit_meta.get("current_version"),
                "kind": kind,
                "status": "draft",
                "summary": summary,
                "created_at": now_iso(),
                "changes": {"mode": "overlay", "path": "changes/"},
                "evidence_required": ["rationale", "validation_notes"],
            },
        )
        (candidate_root / "rationale.md").write_text(
            f"# Rationale\n\n{summary}\n", encoding="utf-8", newline="\n"
        )
        (candidate_root / "notes.md").write_text("# Notes\n", encoding="utf-8", newline="\n")

    update_state(
        unit_root,
        state="active",
        active_candidate=candidate_id,
        reason="candidate_created",
        next_action=f"Develop and validate candidate `{candidate_id}`.",
    )
    return candidate_root
