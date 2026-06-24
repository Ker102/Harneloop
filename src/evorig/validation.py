from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .paths import is_protected_candidate_path, is_secret_path


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


REQUIRED_PATHS = ["unit.yaml", "UNIT_AGENT.md", "candidates", "versions", "provenance"]


def validate_unit(unit_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for required in REQUIRED_PATHS:
        if not (unit_root / required).exists():
            issues.append(ValidationIssue(required, "required path is missing"))

    candidates_root = unit_root / "candidates"
    if candidates_root.exists():
        for changes_root in candidates_root.glob("cand-*/changes"):
            for file_path in changes_root.rglob("*"):
                if not file_path.is_file():
                    continue
                relative = file_path.relative_to(changes_root).as_posix()
                if is_protected_candidate_path(relative):
                    issues.append(ValidationIssue(relative, "candidate attempts to modify a protected path"))
                if is_secret_path(file_path):
                    issues.append(ValidationIssue(relative, "candidate contains a secret-like file"))

    return issues
