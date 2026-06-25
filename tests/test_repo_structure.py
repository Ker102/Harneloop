from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
