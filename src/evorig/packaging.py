from __future__ import annotations

import json
import tarfile
from pathlib import Path

from .errors import EvoRigError
from .state import now_iso
from .yamlio import read_yaml


def package_unit(unit_root: Path, output: Path, profile: str = "thin", version: str | None = None) -> Path:
    if profile != "thin":
        raise EvoRigError("Only the thin package profile is implemented in the core MVP")

    unit_meta = read_yaml(unit_root / "unit.yaml")
    selected_version = version or unit_meta.get("current_version")
    if not selected_version:
        raise EvoRigError("Cannot package a unit before a version has been promoted")

    version_root = unit_root / "versions" / str(selected_version)
    snapshot_root = version_root / "snapshot"
    if not snapshot_root.exists():
        raise EvoRigError(f"Version snapshot does not exist: {selected_version}")

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    package_root_name = f"{unit_meta.get('id', 'unit')}-{selected_version}-{profile}"
    package_manifest = {
        "package_format": "evorig.unit",
        "profile": profile,
        "unit_id": unit_meta.get("id"),
        "version": selected_version,
        "created_at": now_iso(),
        "source": "promoted_snapshot",
    }

    with tarfile.open(output, "w:gz") as archive:
        for source in sorted(snapshot_root.rglob("*")):
            if source.is_file():
                archive.add(source, arcname=f"{package_root_name}/{source.relative_to(snapshot_root).as_posix()}")

        manifest_bytes = json.dumps(package_manifest, indent=2).encode("utf-8") + b"\n"
        info = tarfile.TarInfo(f"{package_root_name}/EVORIG_PACKAGE.json")
        info.size = len(manifest_bytes)
        archive.addfile(info, fileobj=__import__("io").BytesIO(manifest_bytes))

    return output
