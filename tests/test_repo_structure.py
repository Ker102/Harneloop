from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepoStructureTests(unittest.TestCase):
    def test_professional_repo_files_exist(self) -> None:
        required_paths = [
            ".github/pull_request_template.md",
            ".github/workflows/ci.yml",
            ".gitattributes",
            ".gitignore",
            "AGENTS.md",
            "CONTRIBUTING.md",
            "README.md",
            "SECURITY.md",
            "docs/agent-onboarding.md",
            "docs/architecture/core-lifecycle.md",
            "docs/development.md",
            "pyproject.toml",
            "schemas/attempt-plan.schema.json",
            "schemas/artifact-manifest.schema.json",
            "schemas/candidate-evidence.schema.json",
            "schemas/run-record.schema.json",
        ]
        missing = [path for path in required_paths if not (REPO_ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_current_tree_has_no_legacy_product_identity(self) -> None:
        legacy_token = "evo" + "rig"
        tracked = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        ).stdout.decode("utf-8").split("\0")
        text_suffixes = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
        matches: list[str] = []

        for relative in tracked:
            if not relative:
                continue
            if legacy_token in relative.lower():
                matches.append(relative)
                continue
            path = REPO_ROOT / relative
            if path.suffix.lower() not in text_suffixes:
                continue
            if legacy_token in path.read_text(encoding="utf-8").lower():
                matches.append(relative)

        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
