from __future__ import annotations

from typing import Any


ONBOARDING_QUESTIONS: list[dict[str, str]] = [
    {
        "id": "harness_goal",
        "question": "What is the harness goal, and where will the harness be used?",
        "records": "target.task",
    },
    {
        "id": "success_and_failures",
        "question": "What should a good result look like, and what failure patterns matter most?",
        "records": "target.success, target.risks",
    },
    {
        "id": "proof_artifacts",
        "question": "What artifacts prove success or failure, such as renders, screenshots, files, traces, logs, or summaries?",
        "records": "target.artifact_kinds, runs.artifacts",
    },
    {
        "id": "environment_status",
        "question": "Does a testing environment already exist, should the agent connect to one, or should the harness help build it?",
        "records": "environment.mode, environment.interaction_mode",
    },
    {
        "id": "constraints_and_gates",
        "question": "What constraints, protected areas, human review points, or cost/time limits must the harness obey?",
        "records": "environment.notes, promotion.policy, unit constraints",
    },
]


CONTEXT_FIELDS: list[dict[str, str]] = [
    {
        "name": "Target brief",
        "captures": "task, success criteria, artifact kinds, and known risks",
        "command": "evorig target set <unit> --task ... --success ... --artifact-kind ... --risk ...",
    },
    {
        "name": "Environment contract",
        "captures": "existing, assisted, or managed setup plus command, MCP, manual, or custom interaction mode",
        "command": "evorig environment connect <unit> --mode existing --interaction-mode mcp --tool ...",
    },
    {
        "name": "Attempt plan",
        "captures": "the agent-authored workflow for producing and inspecting task-relevant artifacts",
        "command": "evorig attempt plan <unit> --goal ... --method ... --expected-artifact ... --success-check ...",
    },
    {
        "name": "Run and artifact records",
        "captures": "what happened during an attempt and which concrete artifacts were inspected",
        "command": "evorig run start <unit> --task ...; then evorig artifact add <unit> <run-id> <path> --kind ...",
    },
    {
        "name": "Candidate evidence",
        "captures": "why a harness change should or should not be promoted",
        "command": "evorig candidate evidence add <unit> <candidate-id> --kind ... --summary ...",
    },
]


FIRST_ACTIONS: list[str] = [
    "Run `evorig doctor` to confirm the local runtime is usable.",
    "Create a unit with `evorig init-unit <path> --id <id> --name <name> --template artifact-review` unless a blank unit is intentional.",
    "Convert the user's answers into a target brief with `evorig target set`.",
    "Connect or describe the execution environment with `evorig environment connect`.",
    "Create the first baseline attempt with `evorig attempt plan` before changing the harness.",
    "Record runs, artifacts, observations, and candidate evidence before promotion.",
]


def render_onboarding_json() -> dict[str, Any]:
    return {
        "purpose": "Start a new EvoRig harness without relying on chat history.",
        "question_limit": len(ONBOARDING_QUESTIONS),
        "questions": ONBOARDING_QUESTIONS,
        "context_fields": CONTEXT_FIELDS,
        "first_actions": FIRST_ACTIONS,
        "agent_rules": [
            "Ask only the minimal questions needed before the first baseline attempt.",
            "If the environment is tool-driven, declare the tools instead of forcing a single run command.",
            "Do not promote harness changes without concrete evidence or an explicit override.",
            "Use wait and stop states when artifacts, human feedback, or external systems are delayed.",
        ],
    }


def render_onboarding_markdown() -> str:
    data = render_onboarding_json()
    lines = [
        "# EvoRig Agent Onboarding",
        "",
        "Use this checklist when starting a new harness unit. Ask only what is needed to create the first baseline attempt; collect more detail after real artifacts exist.",
        "",
        "## Minimal User Questions",
        "",
    ]

    for index, item in enumerate(data["questions"], start=1):
        lines.append(f"{index}. {item['question']}")
        lines.append(f"   Records: `{item['records']}`")

    lines.extend(["", "## Context Being Collected", ""])
    for item in data["context_fields"]:
        lines.append(f"- {item['name']}: {item['captures']}.")
        lines.append(f"  Command: `{item['command']}`")

    lines.extend(["", "## First Actions", ""])
    for index, action in enumerate(data["first_actions"], start=1):
        lines.append(f"{index}. {action}")

    lines.extend(["", "## Agent Rules", ""])
    for rule in data["agent_rules"]:
        lines.append(f"- {rule}")

    return "\n".join(lines) + "\n"
