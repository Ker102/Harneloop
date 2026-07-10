from __future__ import annotations

import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    ok: bool
    detail: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def check_python() -> DiagnosticCheck:
    version = ".".join(str(part) for part in sys.version_info[:3])
    ok = sys.version_info >= (3, 11)
    return DiagnosticCheck("python", ok, f"Python {version}")


def check_pyyaml() -> DiagnosticCheck:
    try:
        import yaml
    except Exception as exc:  # pragma: no cover - environment-specific detail
        return DiagnosticCheck("pyyaml", False, f"PyYAML import failed: {exc}")
    return DiagnosticCheck("pyyaml", True, f"PyYAML {getattr(yaml, '__version__', 'unknown')}")


def check_git() -> DiagnosticCheck:
    try:
        result = subprocess.run(
            ["git", "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception as exc:  # pragma: no cover - environment-specific detail
        return DiagnosticCheck("git", False, f"git unavailable: {exc}")
    detail = (result.stdout or result.stderr).strip()
    return DiagnosticCheck("git", result.returncode == 0, detail or "git command returned no output")


def check_writable_cwd(cwd: Path) -> DiagnosticCheck:
    probe = cwd / ".harneloop-doctor-write-test"
    try:
        probe.write_text("ok\n", encoding="utf-8", newline="\n")
        probe.unlink()
    except Exception as exc:
        return DiagnosticCheck("writable_cwd", False, f"cannot write to {cwd}: {exc}")
    return DiagnosticCheck("writable_cwd", True, f"writable: {cwd}")


def run_doctor(cwd: Path | None = None) -> list[DiagnosticCheck]:
    root = (cwd or Path.cwd()).resolve()
    return [
        check_python(),
        check_pyyaml(),
        check_git(),
        check_writable_cwd(root),
    ]
