from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .errors import HarneloopError
from .locking import file_lock
from .state import now_iso
from .yamlio import read_yaml, write_yaml


DEFAULT_PREFERENCES: dict[str, Any] = {
    "schema_version": "0.1",
    "agent_behavior": {
        "autonomy_level": "balanced",
        "ask_before_risky_actions": True,
        "promotion_strictness": "evidence_required",
    },
    "validation": {
        "mode": "agent_decides",
        "prefer_visual_artifacts": True,
        "resource_mode": "balanced",
    },
    "export": {
        "default_adapter": "codex",
        "default_package_profile": "thin",
    },
    "runtime": {
        "telemetry_detail": "standard",
        "token_efficiency_mode": False,
        "unit_registry_enabled": True,
    },
}


def harneloop_home(base_dir: Path | None = None) -> Path:
    if base_dir is not None:
        return base_dir.resolve()
    configured = os.environ.get("HARNELOOP_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".harneloop").resolve()


def preferences_path(base_dir: Path | None = None) -> Path:
    return harneloop_home(base_dir) / "preferences.yaml"


def registry_path(base_dir: Path | None = None) -> Path:
    return harneloop_home(base_dir) / "units.yaml"


def _deep_merge(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key, value in defaults.items():
        if isinstance(value, dict):
            merged[key] = _deep_merge(value, overrides.get(key, {}) if isinstance(overrides.get(key), dict) else {})
        else:
            merged[key] = overrides.get(key, value)
    for key, value in overrides.items():
        if key not in merged:
            merged[key] = value
    return merged


def load_preferences(base_dir: Path | None = None) -> dict[str, Any]:
    path = preferences_path(base_dir)
    if not path.exists():
        return _deep_merge(DEFAULT_PREFERENCES, {})
    return _deep_merge(DEFAULT_PREFERENCES, read_yaml(path))


def save_preferences(base_dir: Path | None, preferences: dict[str, Any]) -> dict[str, Any]:
    merged = _deep_merge(DEFAULT_PREFERENCES, preferences)
    write_yaml(preferences_path(base_dir), merged)
    return merged


def update_preference(base_dir: Path | None, dotted_key: str, value: Any) -> dict[str, Any]:
    lock_path = harneloop_home(base_dir) / "locks" / "preferences.lock"
    with file_lock(lock_path):
        preferences = load_preferences(base_dir)
        parts = [part for part in dotted_key.split(".") if part]
        if not parts:
            raise ValueError("Preference key cannot be empty")

        cursor: dict[str, Any] = preferences
        for part in parts[:-1]:
            existing = cursor.setdefault(part, {})
            if not isinstance(existing, dict):
                raise ValueError(f"Cannot set nested preference under non-mapping key `{part}`")
            cursor = existing
        cursor[parts[-1]] = value
        return save_preferences(base_dir, preferences)


def load_registry(base_dir: Path | None = None) -> dict[str, Any]:
    path = registry_path(base_dir)
    if not path.exists():
        return {"schema_version": "0.1", "units": []}
    data = read_yaml(path)
    units = data.get("units")
    if not isinstance(units, list):
        units = []
    return {"schema_version": data.get("schema_version", "0.1"), "units": units}


def save_registry(base_dir: Path | None, registry: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "schema_version": registry.get("schema_version", "0.1"),
        "units": registry.get("units", []),
    }
    write_yaml(registry_path(base_dir), normalized)
    return normalized


def _unit_metadata(unit_path: Path) -> dict[str, Any]:
    data = read_yaml(unit_path / "unit.yaml")
    return {
        "id": data.get("id") or unit_path.name,
        "name": data.get("name") or unit_path.name,
        "current_version": data.get("current_version"),
    }


def register_unit(base_dir: Path | None, unit_path: Path) -> dict[str, Any]:
    resolved = unit_path.resolve()
    if not (resolved / "unit.yaml").exists():
        raise HarneloopError(f"Not a Harneloop harness unit: {resolved}")
    metadata = _unit_metadata(resolved)
    record = {
        "id": metadata["id"],
        "name": metadata["name"],
        "path": str(resolved),
        "current_version": metadata["current_version"],
        "registered_at": now_iso(),
    }
    lock_path = harneloop_home(base_dir) / "locks" / "units.lock"
    with file_lock(lock_path):
        registry = load_registry(base_dir)
        registry["units"] = [
            unit
            for unit in registry["units"]
            if Path(str(unit.get("path", ""))) != resolved and unit.get("id") != metadata["id"]
        ]
        registry["units"].append(record)
        registry["units"].sort(key=lambda item: str(item.get("name", "")).lower())
        save_registry(base_dir, registry)
    return record


def list_registered_units(base_dir: Path | None = None) -> list[dict[str, Any]]:
    return list(load_registry(base_dir)["units"])


def resolve_unit_reference(reference: str | Path, base_dir: Path | None = None) -> Path:
    text = str(reference)
    candidate = Path(reference).expanduser()
    if candidate.exists():
        resolved = candidate.resolve()
        if not (resolved / "unit.yaml").exists():
            raise HarneloopError(f"Not a Harneloop harness unit: {resolved}")
        return resolved

    records = list_registered_units(base_dir)
    exact_id_matches = [record for record in records if str(record.get("id", "")) == text]
    matches = exact_id_matches
    if not matches:
        folded = text.casefold()
        matches = [
            record
            for record in records
            if str(record.get("id", "")).casefold() == folded
            or str(record.get("name", "")).casefold() == folded
        ]
    if not matches and candidate.is_absolute():
        matches = [record for record in records if Path(str(record.get("path", ""))) == candidate]

    if len(matches) > 1:
        ids = ", ".join(sorted(str(record.get("id", "")) for record in matches))
        raise HarneloopError(f"Harness unit reference `{text}` is ambiguous; matching IDs: {ids}")
    if len(matches) == 1:
        registered_path = Path(str(matches[0].get("path", ""))).expanduser()
        if not (registered_path / "unit.yaml").exists():
            raise HarneloopError(
                f"Harness unit `{matches[0].get('id')}` is registered, but its registered path no longer exists: "
                f"{registered_path}. Register its new path with `harneloop units register <path>`."
            )
        return registered_path.resolve()

    raise HarneloopError(
        f"Could not resolve harness unit `{text}` as a local path, registered ID, or registered name. "
        "Run `harneloop units list` or register it with `harneloop units register <path>`."
    )


def remove_registered_unit(base_dir: Path | None, unit_id_or_path: str) -> bool:
    lock_path = harneloop_home(base_dir) / "locks" / "units.lock"
    with file_lock(lock_path):
        registry = load_registry(base_dir)
        before = len(registry["units"])
        registry["units"] = [
            unit
            for unit in registry["units"]
            if unit.get("id") != unit_id_or_path and unit.get("path") != unit_id_or_path
        ]
        save_registry(base_dir, registry)
        return len(registry["units"]) != before
