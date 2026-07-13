from __future__ import annotations

from pathlib import Path

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .adapters import SUPPORTED_ADAPTERS, export_unit
from .attempts import create_attempt_plan
from .diagnostics import run_doctor
from .environment import INTERACTION_MODES, connect_environment, render_environment_status
from .errors import HarneloopError
from .intake import acknowledge_intake, resolve_intake_field
from .onboarding import render_onboarding_markdown
from .preferences import list_registered_units, load_preferences, register_unit, remove_registered_unit, update_preference
from .setup_flow import (
    ENVIRONMENT_STATUS_CHOICES,
    HUMAN_MAIN_MENU,
    SUCCESS_STRATEGIES,
    VALIDATION_PREFERENCES,
    build_guided_setup_plan,
)
from .state import read_state, render_state_markdown
from .target import set_target_brief
from .unit import init_unit


USAGE_CONTEXTS: dict[str, str] = {
    "coding_agent": "Codex, Cursor, Claude Code, or another coding-agent workflow",
    "app_agent": "An agent inside an application or production workflow",
    "research": "A research, prototyping, or experimentation workflow",
    "internal_tool": "An internal tool or automation workflow",
    "not_sure": "Not sure yet",
}


def _menu(console: Console, title: str, items: list[dict[str, str]], default: str = "1") -> str:
    table = Table(title=title, box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Option", style="bold")
    table.add_column("What it does")
    for index, item in enumerate(items, start=1):
        table.add_row(str(index), item["label"], item.get("description", ""))
    console.print(table)
    choice = Prompt.ask("Choose", choices=[str(index) for index in range(1, len(items) + 1)], default=default)
    return items[int(choice) - 1]["id"]


def _mapping_menu(console: Console, title: str, mapping: dict[str, str], default_id: str) -> str:
    items = [{"id": key, "label": value, "description": key} for key, value in mapping.items()]
    default_index = str(list(mapping).index(default_id) + 1) if default_id in mapping else "1"
    return _menu(console, title, items, default=default_index)


def _prompt_non_empty(message: str, default: str | None = None) -> str:
    while True:
        value = Prompt.ask(message, default=default).strip()
        if value:
            return value


def _render_preferences(console: Console, home: Path | None) -> None:
    preferences = load_preferences(home)
    table = Table(title="Harneloop Preferences", box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("Area", style="cyan")
    table.add_column("Setting", style="bold")
    table.add_column("Value")
    for area, values in preferences.items():
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            table.add_row(area, key, str(value))
    console.print(table)


def _render_units(console: Console, home: Path | None) -> list[dict[str, object]]:
    units = list_registered_units(home)
    if not units:
        console.print("[yellow]No registered harness units yet.[/yellow]")
        return units
    table = Table(title="Registered Harness Units", box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("ID")
    table.add_column("Version")
    table.add_column("Path")
    for index, unit in enumerate(units, start=1):
        table.add_row(
            str(index),
            str(unit.get("name", "")),
            str(unit.get("id", "")),
            str(unit.get("current_version") or "unversioned"),
            str(unit.get("path", "")),
        )
    console.print(table)
    return units


def _select_unit(console: Console, home: Path | None) -> Path | None:
    units = _render_units(console, home)
    if not units:
        if not Confirm.ask("Enter a harness unit path manually?", default=True):
            return None
        return Path(_prompt_non_empty("Harness unit path")).expanduser()
    choices = [str(index) for index in range(1, len(units) + 1)] + ["m"]
    choice = Prompt.ask("Choose a unit number, or 'm' for manual path", choices=choices, default="1")
    if choice == "m":
        return Path(_prompt_non_empty("Harness unit path")).expanduser()
    return Path(str(units[int(choice) - 1]["path"]))


def _render_doctor(console: Console) -> None:
    checks = run_doctor(Path.cwd())
    table = Table(title="Diagnostics", box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("Status")
    table.add_column("Check", style="bold")
    table.add_column("Detail")
    for check in checks:
        table.add_row("[green]OK[/green]" if check.ok else "[red]FAIL[/red]", check.name, check.detail)
    console.print(table)


def _create_unit_from_plan(console: Console, home: Path | None, unit_path: Path, plan: dict[str, object]) -> Path:
    unit = init_unit(unit_path, str(plan["unit_id"]), str(plan["unit_name"]), template="artifact-review")
    intake_values = {
        "harness_goal": str(plan["goal"]),
        "usage_context": str(plan["usage_context"]),
        "success_strategy": str(plan["success_strategy"]),
        "validation_preference": str(plan["validation_preference"]),
        "environment_status": str(plan["environment_mode"]),
    }
    for field, value in intake_values.items():
        resolve_intake_field(unit, field, value=value, status="confirmed", source="guided setup")
    acknowledge_intake(
        unit,
        basis="user_confirmed",
        note="The user answered the guided Harneloop setup questions.",
    )
    set_target_brief(
        unit,
        task=str(plan["goal"]),
        success=str(plan["success"]),
        artifact_kind=list(plan["artifact_kinds"]),
        risk=list(plan["risks"]),
    )
    connect_environment(
        unit,
        name=str(plan["environment_name"]),
        mode=str(plan["environment_mode"]),
        interaction_mode=str(plan["interaction_mode"]),
        description=str(plan["environment_description"]),
        notes=list(plan["environment_notes"]),
    )
    create_attempt_plan(
        unit,
        goal=str(plan["attempt_goal"]),
        method=str(plan["attempt_method"]),
        expected_artifact=list(plan["artifact_kinds"]),
        success_check=list(plan["success_checks"]),
        note=list(plan["environment_notes"]),
    )
    register_unit(home, unit)
    console.print(Panel.fit(f"[bold green]Created harness unit[/bold green]\n{unit}", border_style="green"))
    return unit


def run_interactive_setup(home: Path | None = None, console: Console | None = None) -> int:
    console = console or Console()
    console.print(Panel.fit("[bold cyan]Create a New Harneloop Harness Unit[/bold cyan]", border_style="cyan"))

    unit_name = _prompt_non_empty("Harness unit name", default="New Harness Unit")
    goal = _prompt_non_empty("What should this harness help an agent get better at?")
    usage_context = _mapping_menu(console, "Where will it be used?", USAGE_CONTEXTS, "coding_agent")
    success_strategy = _mapping_menu(console, "How should success criteria be handled?", SUCCESS_STRATEGIES, "agent_proposes")
    explicit_success = ""
    if success_strategy == "exact_result":
        explicit_success = _prompt_non_empty("Describe the successful result")
    validation_preference = _mapping_menu(console, "How should results be validated?", VALIDATION_PREFERENCES, "agent_decides")
    environment_status = _mapping_menu(console, "What is the testing/tool environment status?", ENVIRONMENT_STATUS_CHOICES, "not_sure")
    interaction_mode = _mapping_menu(
        console,
        "How will the agent interact with the environment?",
        {mode: mode for mode in sorted(INTERACTION_MODES)},
        "custom",
    )
    constraints = Prompt.ask("Any constraints, review gates, cost limits, or protected areas?", default="").strip()

    plan = build_guided_setup_plan(
        goal=goal,
        usage_context=USAGE_CONTEXTS[usage_context],
        success_strategy=success_strategy,
        validation_preference=validation_preference,
        environment_status=environment_status,
        constraints=constraints,
        explicit_success=explicit_success,
        unit_name=unit_name,
        interaction_mode=interaction_mode,
    )
    default_path = Path.cwd() / "units" / str(plan["unit_id"])
    unit_path = Path(Prompt.ask("Where should the harness unit directory live?", default=str(default_path))).expanduser()

    summary = Table(title="Setup Summary", box=box.SIMPLE_HEAVY, show_header=False)
    summary.add_column("Field", style="cyan")
    summary.add_column("Value")
    summary.add_row("Harness unit", f"{plan['unit_name']} ({plan['unit_id']})")
    summary.add_row("Path", str(unit_path))
    summary.add_row("Success", str(plan["success"]))
    summary.add_row("Validation", VALIDATION_PREFERENCES[str(plan["validation_preference"])])
    summary.add_row("Artifacts", ", ".join(str(item) for item in plan["artifact_kinds"]))
    summary.add_row("Environment", f"{plan['environment_mode']} / {plan['interaction_mode']}")
    console.print(summary)

    if not Confirm.ask("Create this unit now?", default=True):
        console.print("[yellow]Setup cancelled.[/yellow]")
        return 1
    _create_unit_from_plan(console, home, unit_path, plan)
    return 0


def _manage_units(console: Console, home: Path | None) -> None:
    while True:
        choice = _menu(
            console,
            "Harness Unit Management",
            [
                {"id": "list", "label": "List registered harness units", "description": "Show the local harness unit registry."},
                {"id": "register", "label": "Register existing harness unit", "description": "Add a harness unit path to the registry."},
                {"id": "remove", "label": "Remove registry entry", "description": "Forget a harness unit without deleting files."},
                {"id": "back", "label": "Back", "description": "Return to the main menu."},
            ],
        )
        if choice == "back":
            return
        if choice == "list":
            _render_units(console, home)
        elif choice == "register":
            path = Path(_prompt_non_empty("Harness unit path")).expanduser()
            try:
                record = register_unit(home, path)
                console.print(f"[green]Registered[/green] {record['name']} ({record['id']})")
            except Exception as exc:
                console.print(f"[red]Could not register unit:[/red] {exc}")
        elif choice == "remove":
            identifier = _prompt_non_empty("Harness unit ID or full path")
            console.print("[green]Removed.[/green]" if remove_registered_unit(home, identifier) else "[yellow]No match.[/yellow]")


def _manage_settings(console: Console, home: Path | None) -> None:
    while True:
        _render_preferences(console, home)
        choice = _menu(
            console,
            "Settings",
            [
                {"id": "validation", "label": "Validation preference", "description": "How strongly Harneloop should prefer evidence quality vs resources."},
                {"id": "autonomy", "label": "Agent autonomy level", "description": "How independently agents should act inside harness work."},
                {"id": "package", "label": "Default package profile", "description": "Thin, seeded, frozen, or appliance later."},
                {"id": "export", "label": "Default export adapter", "description": "Target agent format."},
                {"id": "tokens", "label": "Token efficiency mode", "description": "Reduce context and telemetry detail when needed."},
                {"id": "back", "label": "Back", "description": "Return to the main menu."},
            ],
        )
        if choice == "back":
            return
        if choice == "validation":
            value = _mapping_menu(console, "Validation preference", VALIDATION_PREFERENCES, "agent_decides")
            update_preference(home, "validation.mode", value)
        elif choice == "autonomy":
            value = _mapping_menu(
                console,
                "Agent autonomy",
                {"conservative": "Conservative", "balanced": "Balanced", "high": "High autonomy"},
                "balanced",
            )
            update_preference(home, "agent_behavior.autonomy_level", value)
        elif choice == "package":
            value = _mapping_menu(
                console,
                "Default package profile",
                {"thin": "Thin", "seeded": "Seeded", "frozen": "Frozen artifact", "appliance": "Appliance"},
                "thin",
            )
            update_preference(home, "export.default_package_profile", value)
        elif choice == "export":
            value = _mapping_menu(console, "Default export adapter", {adapter: adapter for adapter in sorted(SUPPORTED_ADAPTERS)}, "codex")
            update_preference(home, "export.default_adapter", value)
        elif choice == "tokens":
            value = Confirm.ask("Enable token efficiency mode?", default=False)
            update_preference(home, "runtime.token_efficiency_mode", value)


def _show_unit_state(console: Console, home: Path | None) -> None:
    unit = _select_unit(console, home)
    if unit is None:
        return
    try:
        console.print(Markdown(render_state_markdown(read_state(unit))))
        if (unit / "environment" / "contract.yaml").exists():
            console.print(Markdown(render_environment_status(unit)))
    except Exception as exc:
        console.print(f"[red]Could not inspect unit:[/red] {exc}")


def _export_unit_menu(console: Console, home: Path | None) -> None:
    unit = _select_unit(console, home)
    if unit is None:
        return
    adapter = _mapping_menu(console, "Export adapter", {adapter: adapter for adapter in sorted(SUPPORTED_ADAPTERS)}, "codex")
    try:
        output = export_unit(unit, adapter)
        console.print(f"[green]Created export:[/green] {output}")
    except Exception as exc:
        console.print(f"[red]Could not export unit:[/red] {exc}")


def _show_advanced_reference(console: Console) -> None:
    console.print(
        Panel(
            "\n".join(
                [
                    "Agent/script commands:",
                    "",
                    "harneloop onboard",
                    "harneloop init-unit <path> --id <id> --name <name> --template artifact-review",
                    "harneloop target set <unit> --task ... --success ... --artifact-kind ...",
                    "harneloop environment connect <unit> --mode existing --interaction-mode mcp --tool ...",
                    "harneloop attempt plan <unit> --goal ... --method ... --expected-artifact ...",
                    "harneloop run start <unit> --task ...",
                    "harneloop artifact add <unit> <run-id> <path> --kind ...",
                    "harneloop candidate evidence add <unit> <candidate-id> --kind ... --summary ...",
                    "harneloop promote <unit> <candidate-id> --version <version>",
                ]
            ),
            title="Advanced Command Reference",
            border_style="cyan",
        )
    )


def run_interactive_menu(home: Path | None = None, console: Console | None = None) -> int:
    console = console or Console()
    while True:
        console.print(Panel.fit("[bold cyan]Harneloop[/bold cyan]\nSelf-evolving harness units for agents.", border_style="cyan"))
        items = HUMAN_MAIN_MENU + [{"id": "quit", "label": "Quit", "description": "Close Harneloop."}]
        try:
            choice = _menu(console, "What do you want to do?", items)
            if choice == "quit":
                return 0
            if choice == "create_unit":
                run_interactive_setup(home, console)
            elif choice == "manage_units":
                _manage_units(console, home)
            elif choice in {"continue_unit", "review_unit", "manage_candidates"}:
                _show_unit_state(console, home)
            elif choice == "package_export":
                _export_unit_menu(console, home)
            elif choice == "manage_settings":
                _manage_settings(console, home)
            elif choice == "diagnostics":
                _render_doctor(console)
            elif choice == "help":
                console.print(Markdown(render_onboarding_markdown()))
            elif choice == "advanced":
                _show_advanced_reference(console)
        except EOFError:
            console.print("\n[yellow]Exiting Harneloop.[/yellow]")
            return 0
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting Harneloop.[/yellow]")
            return 1
        except HarneloopError as exc:
            console.print(f"[red]Error:[/red] {exc}")
