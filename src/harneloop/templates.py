from __future__ import annotations

from pathlib import Path
from typing import Callable

from .errors import HarneloopError
from .yamlio import write_yaml


TemplateApplier = Callable[[Path], None]


def apply_blank_template(unit_root: Path) -> None:
    return None


def apply_artifact_review_template(unit_root: Path) -> None:
    (unit_root / "agent-facing" / "principles.md").write_text(
        "\n".join(
            [
                "# Artifact Review Principles",
                "",
                "- Inspect real artifacts before judging task success.",
                "- Prefer deterministic validators when the task has measurable requirements.",
                "- Use visual or structured artifact review when deterministic checks are incomplete.",
                "- Add evidence before promoting harness changes.",
                "- Treat missing artifact visibility as a harness problem, not only an agent failure.",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    write_yaml(
        unit_root / "observers" / "contracts.yaml",
        {
            "schema_version": "0.1",
            "observers": [
                {
                    "id": "artifact-presence",
                    "description": "Confirm expected output artifacts exist and are readable.",
                    "inputs": ["runtime/artifacts/**"],
                    "outputs": ["artifact_manifest"],
                },
                {
                    "id": "artifact-summary",
                    "description": "Summarize artifact content or metadata for later critique.",
                    "inputs": ["artifact_manifest"],
                    "outputs": ["observer_notes"],
                },
            ],
        },
    )
    write_yaml(
        unit_root / "validators" / "contracts.yaml",
        {
            "schema_version": "0.1",
            "validators": [
                {
                    "id": "artifact-exists",
                    "description": "Fail when a required artifact was not captured.",
                    "inputs": ["run_record"],
                    "required": True,
                },
                {
                    "id": "evidence-present",
                    "description": "Fail promotion when no candidate evidence exists.",
                    "inputs": ["candidate"],
                    "required": True,
                },
            ],
        },
    )
    write_yaml(
        unit_root / "regression-cases" / "artifact-smoke.yaml",
        {
            "schema_version": "0.1",
            "id": "artifact-smoke",
            "task": "Create a small text artifact and capture it in a run record.",
            "expected_artifacts": [{"kind": "text", "description": "Smoke-test output"}],
            "promotion_expectation": "Candidate cannot promote until evidence is recorded.",
        },
    )


TEMPLATES: dict[str, TemplateApplier] = {
    "blank": apply_blank_template,
    "artifact-review": apply_artifact_review_template,
}


def list_templates() -> list[str]:
    return sorted(TEMPLATES)


def apply_template(unit_root: Path, template: str) -> None:
    try:
        applier = TEMPLATES[template]
    except KeyError as exc:
        supported = ", ".join(list_templates())
        raise HarneloopError(f"Unknown template `{template}`. Expected one of: {supported}") from exc
    applier(unit_root)
