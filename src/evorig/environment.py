from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import EvoRigError
from .state import now_iso, update_state
from .versioning import ensure_unit
from .yamlio import read_yaml, write_yaml


ENVIRONMENT_MODES = {"existing", "assisted", "managed"}
INTERACTION_MODES = {"command", "mcp", "manual", "custom"}


def normalize_notes(notes: list[str] | tuple[str, ...] | None) -> list[str]:
    return [note for note in (notes or []) if note]


def normalize_tools(tools: list[str] | tuple[str, ...] | None) -> list[str]:
    return [tool for tool in (tools or []) if tool]


def environment_root(unit_root: Path) -> Path:
    return unit_root / "environment"


def contract_path(unit_root: Path) -> Path:
    return environment_root(unit_root) / "contract.yaml"


def connect_environment(
    unit_root: Path,
    name: str,
    mode: str,
    description: str,
    run_command: str | None = None,
    artifact_path: str | None = None,
    interaction_mode: str = "command",
    tool: list[str] | tuple[str, ...] | None = None,
    notes: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    unit_root = unit_root.resolve()
    ensure_unit(unit_root)
    if mode not in ENVIRONMENT_MODES:
        supported = ", ".join(sorted(ENVIRONMENT_MODES))
        raise EvoRigError(f"Unknown environment mode `{mode}`. Expected one of: {supported}")
    if interaction_mode not in INTERACTION_MODES:
        supported = ", ".join(sorted(INTERACTION_MODES))
        raise EvoRigError(f"Unknown interaction mode `{interaction_mode}`. Expected one of: {supported}")

    root = environment_root(unit_root)
    root.mkdir(parents=True, exist_ok=True)
    contract: dict[str, Any] = {
        "schema_version": "0.1",
        "name": name,
        "mode": mode,
        "interaction_mode": interaction_mode,
        "description": description,
        "run_command": run_command,
        "artifact_path": artifact_path,
        "tools": normalize_tools(tool),
        "notes": normalize_notes(notes),
        "created_at": now_iso(),
    }
    write_yaml(contract_path(unit_root), contract)
    (root / "README.md").write_text(render_environment_status(unit_root, contract), encoding="utf-8", newline="\n")
    (root / "GETTING_STARTED.md").write_text(render_getting_started(contract), encoding="utf-8", newline="\n")
    update_state(
        unit_root,
        reason="environment_connected",
        next_action="Run a baseline task and capture artifacts through the declared environment contract.",
    )
    return contract


def read_environment_contract(unit_root: Path) -> dict[str, Any]:
    path = contract_path(unit_root)
    if not path.exists():
        raise EvoRigError("No environment contract exists. Run `evorig environment connect` first.")
    return read_yaml(path)


def render_environment_status(unit_root: Path, contract: dict[str, Any] | None = None) -> str:
    data = contract or read_environment_contract(unit_root)
    mode = data.get("mode")
    interaction_mode = data.get("interaction_mode") or "command"
    if mode == "existing":
        mode_guidance = "Connect to the existing environment. Do not rebuild it unless checks fail or the user asks."
    elif mode == "assisted":
        mode_guidance = "Assist setup by proposing missing commands, dependencies, or artifact capture steps."
    else:
        mode_guidance = "Managed setup is allowed, but every infrastructure change should be explicit."

    if interaction_mode == "mcp":
        interaction_guidance = "Use the declared tools exposed by the MCP server. Do not search for a single run command unless the contract adds one."
    elif interaction_mode == "command":
        interaction_guidance = "Use the declared run command, then collect artifacts from the declared artifact path."
    elif interaction_mode == "manual":
        interaction_guidance = "Ask the user or target agent to perform the action, then capture resulting artifacts."
    else:
        interaction_guidance = "Follow the custom environment notes and capture artifacts through the declared paths."

    lines = [
        "# Environment Contract",
        "",
        f"- Name: {data.get('name')}",
        f"- Mode: `{mode}`",
        f"- Tool interface: `{interaction_mode}`",
        f"- Description: {data.get('description')}",
        f"- Run command: `{data.get('run_command') or 'not declared'}`",
        f"- Artifact path: `{data.get('artifact_path') or 'not declared'}`",
        "",
        "## Mode Guidance",
        "",
        mode_guidance,
        "",
        "## Interaction Guidance",
        "",
        interaction_guidance,
    ]
    tools = data.get("tools") or []
    if tools:
        lines.extend(["", "## Declared Tools", ""])
        lines.extend(f"- `{tool}`" for tool in tools)
    notes = data.get("notes") or []
    if notes:
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in notes)
    return "\n".join(lines) + "\n"


def render_getting_started(contract: dict[str, Any]) -> str:
    interaction_mode = contract.get("interaction_mode") or "command"
    lines = [
        "# Environment Getting Started",
        "",
        "Use this file to orient an agent before the first baseline run.",
        "",
        "## First Steps",
        "",
        "1. Read `target/brief.yaml` and `target/TEST_SUGGESTIONS.md`.",
        "2. Read `environment/contract.yaml` and this file.",
        "3. Perform a baseline run before changing the harness.",
        "4. Capture artifacts with `evorig artifact add`.",
        "5. Add candidate evidence before promotion.",
    ]
    if interaction_mode == "mcp":
        tools = contract.get("tools") or []
        lines.extend(
            [
                "",
                "## MCP Tool Workflow",
                "",
                "This environment is tool-driven. The agent should interact with the existing MCP server and addon tools.",
                "",
                "Suggested baseline run:",
                "",
                "1. Use the MCP tools to create or modify the artifact-producing scene/task.",
                "2. Use the MCP tools to render, capture screenshots, or export structured summaries.",
                "3. Add each produced artifact to the EvoRig run record.",
                "4. Compare the artifacts against the target success criteria.",
            ]
        )
        if tools:
            lines.extend(["", "Declared tools:"])
            lines.extend(f"- `{tool}`" for tool in tools)
    elif interaction_mode == "command":
        lines.extend(
            [
                "",
                "## Command Workflow",
                "",
                f"Run command: `{contract.get('run_command') or 'not declared'}`",
                f"Artifact path: `{contract.get('artifact_path') or 'not declared'}`",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Custom Workflow",
                "",
                "Follow the environment notes and capture artifacts into EvoRig run records.",
            ]
        )
    return "\n".join(lines) + "\n"
