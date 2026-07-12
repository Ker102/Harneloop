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
        "name": "Operational map",
        "captures": "the current working understanding of workflow, artifacts, evidence, environment assumptions, reset paths, capability gaps, constraints, and open questions",
        "command": "update operational-map.md after inspecting the real workspace and whenever the unit workflow changes",
    },
    {
        "name": "Target brief",
        "captures": "task, success criteria, artifact kinds, and known risks",
        "command": "harneloop target set <harness-unit> --task ... --success ... --artifact-kind ... --risk ...",
    },
    {
        "name": "Environment contract",
        "captures": "existing, assisted, or managed setup plus command, MCP, manual, or custom interaction mode",
        "command": "harneloop environment connect <harness-unit> --mode existing --interaction-mode mcp --tool ...",
    },
    {
        "name": "Attempt plan",
        "captures": "the agent-authored workflow for producing and inspecting task-relevant artifacts",
        "command": "harneloop attempt plan <harness-unit> --goal ... --method ... --expected-artifact ... --success-check ...",
    },
    {
        "name": "Run and artifact records",
        "captures": "what happened during an attempt and which concrete artifacts were inspected",
        "command": "harneloop run start <harness-unit> --task ...; then harneloop artifact add <harness-unit> <run-id> <path> --kind ...",
    },
    {
        "name": "Candidate evidence",
        "captures": "why a harness change should or should not be promoted",
        "command": "harneloop candidate evidence add <harness-unit> <candidate-id> --kind ... --summary ...",
    },
]


FIRST_ACTIONS: list[str] = [
    "Run `harneloop doctor` to confirm the local runtime is usable.",
    "Create a harness unit with `harneloop init-unit <path> --id <id> --name <name> --template artifact-review` unless a blank harness unit is intentional.",
    "Read `operational-map.md` and update it as the current orientation for this harness unit.",
    "Convert the user's answers into a target brief with `harneloop target set`.",
    "Connect or describe the execution environment with `harneloop environment connect`.",
    "Create the first baseline attempt with `harneloop attempt plan` before changing the harness.",
    "Record runs, artifacts, observations, and candidate evidence before promotion.",
]


def render_onboarding_json() -> dict[str, Any]:
    return {
        "purpose": "Start a new Harneloop harness without relying on chat history.",
        "question_limit": len(ONBOARDING_QUESTIONS),
        "questions": ONBOARDING_QUESTIONS,
        "optional_follow_ups": OPTIONAL_ONBOARDING_FOLLOW_UPS,
        "context_fields": CONTEXT_FIELDS,
        "first_actions": FIRST_ACTIONS,
        "agent_rules": [
            "Ask only the minimal questions needed before the first baseline attempt.",
            "Treat success criteria and artifact choices as guided options; the user does not need to design validation up front.",
            "Use `operational-map.md` as context and navigation, not as a rigid procedure; update it when workflow, evidence needs, or environment assumptions change.",
            "Harneloop does not discover environment endpoints, tools, commands, or artifact paths by itself; the onboarding agent must inspect the workspace and record that mapping.",
            "If the environment is tool-driven, declare the tools instead of forcing a single run command.",
            "Operating-agent capabilities are what the current agent can actually use, such as terminal, filesystem, browser, MCPs, package managers, visual inspection, or database access.",
            "Unit/target-agent tools are tools designed into the harness unit or provided to the target agent; keep them separate from the operating agent's own capabilities.",
            "When a capability is missing, state what is missing, why it matters, what tool or dependency would help, and what risk, cost, auth, or security change it introduces.",
            "Capability additions should be justified by observed bottlenecks, failed attempts, missing artifacts, or clear expected improvement, not added speculatively.",
            "Optimize for the best verified result, not a from-scratch implementation; inspect and reuse suitable project-native or external tools, open-source libraries, agent skills, MCP servers, validators, datasets, examples, documentation, research, and prior harness work.",
            "Record the source, relevant version, purpose, license or attribution obligations, compatibility assumptions, and evidence of value for reused material; review executable third-party material before trusting it.",
            "Low-risk local capabilities can be installed, enabled, or built when the environment allows it; larger dependencies, auth, secrets, external access, paid services, or security-impacting changes should be proposed first.",
            "Aim to run repeated testing/improvement loops without requiring the user to restart apps, reinstall addons, reset services, or collect files; if automating the environment is reasonable, implement or document it.",
            "Ask the user before environment automation when the automation is risky, unclear, or too expensive/time-consuming.",
            "Do not promote harness changes without concrete evidence or an explicit override.",
            "Use wait and stop states when artifacts, human feedback, or external systems are delayed.",
        ],
    }


def render_onboarding_markdown() -> str:
    data = render_onboarding_json()
    lines = [
        "# Harneloop Agent Onboarding",
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
