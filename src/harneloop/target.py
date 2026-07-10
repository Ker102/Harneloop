from __future__ import annotations

from pathlib import Path
from typing import Any

from .state import now_iso, update_state
from .versioning import ensure_unit
from .yamlio import write_yaml


def normalize_list(value: list[str] | tuple[str, ...] | None) -> list[str]:
    return [item for item in (value or []) if item]


def render_test_suggestions(brief: dict[str, Any]) -> str:
    artifact_kinds = brief.get("artifact_kinds") or []
    risks = brief.get("risks") or []
    lines = [
        "# Starter Test Suggestions",
        "",
        "These are starting points for the agent. They should be refined into concrete regression cases.",
        "",
        "## Target Task",
        "",
        brief["task"],
        "",
        "## Success Signal",
        "",
        brief["success"],
        "",
        "## Suggested First Tests",
        "",
        "- Baseline run: capture current behavior before changing the harness.",
        "- Artifact capture test: verify every expected artifact is collected into `runtime/artifacts/`.",
        "- Evidence gate test: verify candidate promotion fails without evidence and succeeds with relevant evidence.",
    ]
    for kind in artifact_kinds:
        lines.append(f"- `{kind}` review: inspect and summarize the captured `{kind}` artifact.")
    for risk in risks:
        lines.append(f"- Risk regression: create a case that would expose `{risk}`.")

    lines.extend(
        [
            "",
            "## Agent Questions To Ask If Missing",
            "",
            "- Is there already a working test environment for this task?",
            "- Is the task run through a command, tools, a manual flow, or a custom workflow?",
            "- If tool-driven, which tools should the agent use?",
            "- Where are artifacts written?",
            "- Which artifacts should count as evidence?",
            "- What failures are common enough to become regression cases?",
        ]
    )
    return "\n".join(lines) + "\n"


def set_target_brief(
    unit_root: Path,
    task: str,
    success: str,
    artifact_kind: list[str] | tuple[str, ...] | None = None,
    risk: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    ensure_unit(unit_root)
    if not task.strip():
        raise ValueError("Target task cannot be empty")
    if not success.strip():
        raise ValueError("Success description cannot be empty")

    target_root = unit_root / "target"
    target_root.mkdir(parents=True, exist_ok=True)
    brief: dict[str, Any] = {
        "schema_version": "0.1",
        "task": task,
        "success": success,
        "artifact_kinds": normalize_list(artifact_kind),
        "risks": normalize_list(risk),
        "created_at": now_iso(),
    }
    write_yaml(target_root / "brief.yaml", brief)
    (target_root / "TEST_SUGGESTIONS.md").write_text(
        render_test_suggestions(brief),
        encoding="utf-8",
        newline="\n",
    )
    update_state(
        unit_root,
        reason="target_brief_updated",
        next_action="Connect or verify the testing environment, then create a baseline run.",
    )
    return brief
