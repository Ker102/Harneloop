from __future__ import annotations

from pathlib import Path

from .errors import EvoRigError
from .state import read_state
from .versioning import ensure_unit
from .yamlio import read_yaml


SUPPORTED_ADAPTERS = {"generic", "codex", "cursor"}


def collect_agent_markdown(unit_root: Path) -> str:
    sections: list[str] = []
    unit_agent = unit_root / "UNIT_AGENT.md"
    if unit_agent.exists():
        sections.append(unit_agent.read_text(encoding="utf-8").strip())

    agent_facing = unit_root / "agent-facing"
    if agent_facing.exists():
        for path in sorted(agent_facing.rglob("*.md")):
            sections.append(path.read_text(encoding="utf-8").strip())

    return "\n\n---\n\n".join(section for section in sections if section)


def export_body(unit_root: Path, adapter: str) -> str:
    unit_meta = read_yaml(unit_root / "unit.yaml")
    state = read_state(unit_root)
    instructions = collect_agent_markdown(unit_root)
    current_version = unit_meta.get("current_version") or "none"

    return "\n".join(
        [
            f"# {unit_meta.get('name', unit_meta.get('id', 'EvoRig Unit'))}",
            "",
            f"Export adapter: `{adapter}`",
            f"Unit id: `{unit_meta.get('id', 'unknown')}`",
            f"Current version: `{current_version}`",
            f"Lifecycle state: `{state.get('state', 'unknown')}`",
            "",
            "## Harness Instructions",
            "",
            instructions or "No agent-facing instructions have been promoted yet.",
            "",
            "## Operating Rules",
            "",
            "- Treat these instructions as the promoted harness for this task family.",
            "- Do not edit the source harness unit directly from this export.",
            "- Improvements should be proposed as EvoRig candidates and promoted through evidence gates.",
            "- Runtime traces, raw artifacts, local caches, and secrets are not part of this export.",
        ]
    ) + "\n"


def export_unit(unit_root: Path, adapter: str, output: Path | None = None) -> Path:
    unit_root = unit_root.resolve()
    ensure_unit(unit_root)
    if adapter not in SUPPORTED_ADAPTERS:
        supported = ", ".join(sorted(SUPPORTED_ADAPTERS))
        raise EvoRigError(f"Unsupported adapter `{adapter}`. Expected one of: {supported}")

    export_root = (output or (unit_root / "exports" / adapter)).resolve()
    export_root.mkdir(parents=True, exist_ok=True)
    body = export_body(unit_root, adapter)

    if adapter == "codex":
        (export_root / "AGENTS.md").write_text(body, encoding="utf-8", newline="\n")
    elif adapter == "cursor":
        cursor_body = "---\ndescription: EvoRig exported harness unit\nalwaysApply: false\n---\n\n" + body
        (export_root / "evorig-unit.mdc").write_text(cursor_body, encoding="utf-8", newline="\n")
    else:
        (export_root / "UNIT_AGENT.md").write_text(body, encoding="utf-8", newline="\n")

    return export_root
