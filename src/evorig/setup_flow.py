from __future__ import annotations

import re
from typing import Any


HUMAN_MAIN_MENU: list[dict[str, str]] = [
    {
        "id": "create_unit",
        "label": "Create a new harness unit",
        "description": "Guided setup for a new target task.",
    },
    {
        "id": "manage_units",
        "label": "List and manage units",
        "description": "View registered units, register existing units, or remove registry entries.",
    },
    {
        "id": "continue_unit",
        "label": "Continue an active unit",
        "description": "Open the current state and next action for an existing unit.",
    },
    {
        "id": "review_unit",
        "label": "Review status, runs, artifacts, and evidence",
        "description": "Inspect what has happened and what evidence exists.",
    },
    {
        "id": "manage_candidates",
        "label": "Manage candidates, versions, and rollback",
        "description": "Review candidate lifecycle and promoted snapshots.",
    },
    {
        "id": "package_export",
        "label": "Package or export a unit",
        "description": "Create portable packages or target-agent exports.",
    },
    {
        "id": "manage_settings",
        "label": "Manage settings and preferences",
        "description": "Configure agent behavior, validation style, exports, and runtime defaults.",
    },
    {
        "id": "diagnostics",
        "label": "Run diagnostics",
        "description": "Check local EvoRig prerequisites.",
    },
    {
        "id": "help",
        "label": "Help me understand EvoRig",
        "description": "Explain the workflow and next recommended command.",
    },
    {
        "id": "advanced",
        "label": "Advanced command reference",
        "description": "Show automation commands for agents and scripts.",
    },
]


SUCCESS_STRATEGIES: dict[str, str] = {
    "agent_proposes": "Let the agent propose success criteria",
    "exact_result": "I know the exact successful result",
    "after_baseline": "Decide after the first baseline attempt",
}


VALIDATION_PREFERENCES: dict[str, str] = {
    "best_quality": "Best validation quality",
    "visual_artifact_first": "Visual or artifact-first validation",
    "balanced": "Balanced validation",
    "resource_efficient": "Resource-efficient validation",
    "agent_decides": "Let the agent decide per task",
}


ENVIRONMENT_STATUS_CHOICES: dict[str, str] = {
    "existing": "A testing or tool environment already exists",
    "partial": "Part of the environment exists",
    "build_new": "The harness should help build one",
    "not_sure": "Not sure yet",
}


VISUAL_TERMS = {
    "3d",
    "blender",
    "canvas",
    "diagram",
    "image",
    "render",
    "scene",
    "spatial",
    "svg",
    "ui",
    "visual",
}
CODE_TERMS = {
    "api",
    "cli",
    "code",
    "function",
    "library",
    "package",
    "program",
    "script",
    "test",
}


def unit_id_from_name(name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    normalized = re.sub(r"-+", "-", normalized)
    return normalized or "new-harness-unit"


def _contains_any(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def suggest_artifact_kinds(goal: str, validation_preference: str) -> list[str]:
    visual = _contains_any(goal, VISUAL_TERMS)
    code = _contains_any(goal, CODE_TERMS)

    if validation_preference == "agent_decides":
        return ["agent_selected_artifacts", "run_trace", "decision_notes"]

    if validation_preference == "resource_efficient":
        artifacts = ["structured_summary", "run_trace"]
        if code:
            artifacts.append("test_output")
        else:
            artifacts.append("lightweight_check")
        return artifacts

    if validation_preference == "visual_artifact_first":
        if "svg" in goal.lower():
            return ["rendered_image", "browser_screenshot", "source_svg", "visual_review_notes"]
        if visual:
            return ["render", "screenshot", "visual_review_notes", "scene_summary"]
        return ["primary_artifact", "artifact_review_notes", "run_trace"]

    if validation_preference == "best_quality":
        if "svg" in goal.lower():
            return ["source_svg", "rendered_image", "browser_screenshot", "visual_review_notes", "run_trace"]
        if visual:
            return ["render", "screenshot", "scene_summary", "visual_review_notes", "run_trace"]
        if code:
            return ["test_output", "execution_log", "trace_summary", "regression_case"]
        return ["primary_artifact", "structured_summary", "run_trace", "review_notes"]

    artifacts = ["primary_artifact", "structured_summary", "run_trace"]
    if visual:
        artifacts.insert(1, "screenshot")
    if code:
        artifacts.insert(1, "test_output")
    return artifacts


def _success_text(success_strategy: str, explicit_success: str | None) -> str:
    if success_strategy == "exact_result" and explicit_success and explicit_success.strip():
        return explicit_success.strip()
    if success_strategy == "after_baseline":
        return "Success criteria should be finalized after the first baseline attempt reveals the current failure modes."
    return "The agent should propose success criteria from the target goal, baseline artifacts, and observed failure patterns."


def _environment_mode(environment_status: str) -> str:
    if environment_status == "existing":
        return "existing"
    if environment_status == "build_new":
        return "managed"
    return "assisted"


def build_guided_setup_plan(
    *,
    goal: str,
    usage_context: str,
    success_strategy: str,
    validation_preference: str,
    environment_status: str,
    constraints: str = "",
    explicit_success: str | None = None,
    unit_name: str | None = None,
    unit_id: str | None = None,
    interaction_mode: str | None = None,
) -> dict[str, Any]:
    clean_goal = goal.strip()
    if not clean_goal:
        raise ValueError("Harness goal cannot be empty")

    name = (unit_name or clean_goal[:64]).strip()
    resolved_unit_id = unit_id or unit_id_from_name(name)
    artifacts = suggest_artifact_kinds(clean_goal, validation_preference)
    environment_mode = _environment_mode(environment_status)
    resolved_interaction_mode = interaction_mode or "custom"
    notes = [
        f"Usage context: {usage_context}",
        f"Validation preference: {VALIDATION_PREFERENCES.get(validation_preference, validation_preference)}",
        f"Environment status: {ENVIRONMENT_STATUS_CHOICES.get(environment_status, environment_status)}",
    ]
    if constraints.strip():
        notes.append(constraints.strip())

    return {
        "unit_id": resolved_unit_id,
        "unit_name": name,
        "goal": clean_goal,
        "usage_context": usage_context.strip() or "Not specified",
        "success": _success_text(success_strategy, explicit_success),
        "success_strategy": success_strategy,
        "validation_preference": validation_preference,
        "artifact_kinds": artifacts,
        "risks": ["success criteria may need revision after the baseline attempt"],
        "environment_name": f"{name} environment",
        "environment_mode": environment_mode,
        "interaction_mode": resolved_interaction_mode,
        "environment_description": "Guided setup captured the current environment status. The agent should refine this contract after inspecting the real workspace.",
        "environment_notes": notes,
        "attempt_goal": clean_goal,
        "attempt_method": "Use the declared environment and validation preference to create a baseline artifact-producing attempt before changing the harness.",
        "success_checks": [
            "A baseline attempt is recorded.",
            "Expected artifacts are captured into EvoRig.",
            "The agent writes observations before proposing harness changes.",
        ],
    }
