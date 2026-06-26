from __future__ import annotations

from typing import Any


ONBOARDING_QUESTIONS: list[dict[str, str]] = [
    {
        "id": "harness_goal",
        "question": "What should this harness help an agent get better at?",
        "records": "target.task",
    },
    {
        "id": "usage_context",
        "question": "Where will the harness be used, such as a coding-agent workflow, an app agent, research, or internal automation?",
        "records": "target.context, environment.notes",
    },
    {
        "id": "success_strategy",
        "question": "How should success criteria be handled?",
        "records": "target.success",
        "suggested_answers": "let the agent propose criteria, provide exact success criteria, or decide after the first baseline attempt",
    },
    {
        "id": "validation_preference",
        "question": "How should results be validated?",
        "records": "target.artifact_kinds, preferences.validation.mode, runs.artifacts",
        "suggested_answers": "best validation quality, visual/artifact-first, balanced, resource-efficient, or let the agent decide",
    },
    {
        "id": "environment_status",
        "question": "Does a testing environment already exist, partly exist, need to be built, or is that not clear yet?",
        "records": "environment.mode, environment.interaction_mode",
    },
]


OPTIONAL_ONBOARDING_FOLLOW_UPS: list[dict[str, str]] = [
    {
        "id": "constraints_and_gates",
        "question": "Are there constraints, protected areas, human review points, or cost/time limits the harness must obey?",
        "records": "environment.notes, promotion.policy, unit constraints",
    },
]


CONTEXT_FIELDS: list[dict[str, str]] = [
    {
        "name": "Target brief",
        "captures": "task, success criteria, artifact kinds, and known risks",
        "command": "evorig target set <harness-unit> --task ... --success ... --artifact-kind ... --risk ...",
    },
    {
        "name": "Environment contract",
        "captures": "existing, assisted, or managed setup plus command, MCP, manual, or custom interaction mode",
        "command": "evorig environment connect <harness-unit> --mode existing --interaction-mode mcp --tool ...",
    },
    {
        "name": "Attempt plan",
        "captures": "the agent-authored workflow for producing and inspecting task-relevant artifacts",
        "command": "evorig attempt plan <harness-unit> --goal ... --method ... --expected-artifact ... --success-check ...",
    },
    {
        "name": "Run and artifact records",
        "captures": "what happened during an attempt and which concrete artifacts were inspected",
        "command": "evorig run start <harness-unit> --task ...; then evorig artifact add <harness-unit> <run-id> <path> --kind ...",
    },
    {
        "name": "Candidate evidence",
        "captures": "why a harness change should or should not be promoted",
        "command": "evorig candidate evidence add <harness-unit> <candidate-id> --kind ... --summary ...",
    },
]


FIRST_ACTIONS: list[str] = [
    "Run `evorig doctor` to confirm the local runtime is usable.",
    "Create a harness unit with `evorig init-unit <path> --id <id> --name <name> --template artifact-review` unless a blank harness unit is intentional.",
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
        "optional_follow_ups": OPTIONAL_ONBOARDING_FOLLOW_UPS,
        "context_fields": CONTEXT_FIELDS,
        "first_actions": FIRST_ACTIONS,
        "agent_rules": [
            "Ask only the minimal questions needed before the first baseline attempt.",
            "Treat success criteria and artifact choices as guided options; the user does not need to design validation up front.",
            "EvoRig does not discover environment endpoints, tools, commands, or artifact paths by itself; the onboarding agent must inspect the workspace and record that mapping.",
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
        if item.get("suggested_answers"):
            lines.append(f"   Suggested answers: {item['suggested_answers']}")

    lines.extend(["", "## Optional Follow-Ups", ""])
    for item in data["optional_follow_ups"]:
        lines.append(f"- {item['question']}")
        lines.append(f"  Records: `{item['records']}`")

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
