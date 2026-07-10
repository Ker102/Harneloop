from __future__ import annotations

from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".evolve",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "attempts",
    "candidates",
    "experiments",
    "runtime",
    "versions",
}

SECRET_NAMES = {".env", "credentials.json"}
SECRET_SUFFIXES = {".pem", ".key"}
PROTECTED_EXACT = {"unit.yaml"}
PROTECTED_PREFIXES = ("versions/", "provenance/", ".evolve/", "candidates/", "runtime/")


def to_posix(path: Path) -> str:
    return path.as_posix()


def relative_posix(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def is_secret_path(path: Path) -> bool:
    return path.name in SECRET_NAMES or path.suffix.lower() in SECRET_SUFFIXES


def is_protected_candidate_path(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/").lstrip("/")
    if normalized in PROTECTED_EXACT:
        return True
    return any(normalized.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def packageable_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in relative_parts):
            continue
        if is_secret_path(path):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())
