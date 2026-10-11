from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_i18n import compare_documents, source_hash, validate_tree


SOURCE = '# Guide\n\nUse `harneloop doctor`.\n\n## Safety\n\nPublic alpha.\n\n```bash\nharneloop setup\n```\n'
MIRROR = '<a id="guide"></a>\n# Guía\n\nUsa `harneloop doctor`.\n\n<a id="safety"></a>\n## Seguridad\n\nAlfa pública.\n\n```bash\nharneloop setup\n```\n'


class TranslationValidatorTests(unittest.TestCase):
    def test_repository_translations_are_current(self) -> None:
        root = Path(__file__).resolve().parents[1]
        errors, coverage = validate_tree(root)
        self.assertEqual(errors, [], "\n".join(errors))
        self.assertTrue(coverage)
        for locale, (complete, total) in coverage.items():
            self.assertEqual(complete, total, f"{locale}: incomplete maintained documentation")

    def test_equivalent_structure_and_code(self) -> None:
        self.assertEqual(compare_documents(SOURCE, MIRROR), [])

    def test_source_hash_ignores_checkout_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.md"
            path.write_bytes(SOURCE.encode("utf-8"))
            digest = source_hash(path)
            path.write_bytes(SOURCE.replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(source_hash(path), digest)

    def test_changed_code_is_rejected(self) -> None:
        errors = compare_documents(SOURCE, MIRROR.replace("harneloop setup", "harneloop init"))
        self.assertTrue(any("fenced code" in error for error in errors))

    def test_unclosed_fence_is_rejected(self) -> None:
        self.assertTrue(any("unclosed" in error for error in compare_documents(SOURCE, MIRROR.rstrip()[:-3])))

    def test_inline_command_is_preserved(self) -> None:
        self.assertTrue(any("inline code" in error for error in compare_documents(SOURCE, MIRROR.replace("harneloop doctor", "harneloop test"))))

    def test_missing_sections_are_rejected(self) -> None:
        self.assertTrue(compare_documents(SOURCE, MIRROR.replace("## Seguridad", "Seguridad")))

    def test_external_urls_are_preserved(self) -> None:
        self.assertTrue(any("external" in error for error in compare_documents(SOURCE + "\n[Site](https://example.org/a)\n", MIRROR + "\n[Sitio](https://example.org/b)\n")))

    def test_reference_links_and_html_assets_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_tree(root, MIRROR + '\n[Missing][ref]\n\n[ref]: missing.md\n<img src="missing.png" />\n')
            errors, _ = validate_tree(root)
            self.assertTrue(any("missing.md" in error for error in errors))
            self.assertTrue(any("missing.png" in error for error in errors))

    def make_tree(self, root: Path, mirror: str = MIRROR) -> None:
        (root / "docs/i18n/es").mkdir(parents=True)
        (root / "docs/guide.md").write_text(SOURCE, encoding="utf-8")
        (root / "docs/i18n/es/guide.md").write_text(mirror, encoding="utf-8")
        digest = source_hash(root / "docs/guide.md")
        manifest = {
            "schema_version": 1,
            "locales": ["es"],
            "sources": [{
                "path": "docs/guide.md", "sha256": digest,
                "mirrors": {"es": {"path": "docs/i18n/es/guide.md", "status": "complete", "source_sha256": digest}},
            }],
        }
        # Match the prescribed repository-relative mirror layout.
        (root / "docs/i18n/es/docs").mkdir()
        (root / "docs/i18n/es/guide.md").rename(root / "docs/i18n/es/docs/guide.md")
        manifest["sources"][0]["mirrors"]["es"]["path"] = "docs/i18n/es/docs/guide.md"
        (root / "docs/i18n/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def test_tree_links_fragments_and_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_tree(root)
            self.assertEqual(validate_tree(root)[0], [])
            mirror = root / "docs/i18n/es/docs/guide.md"
            mirror.write_text(MIRROR + '\n[Safety](#safety)\n[Absent](#absent)\n[Missing](missing.md)\n', encoding="utf-8")
            errors, _ = validate_tree(root)
            self.assertTrue(any("#absent" in error for error in errors))
            self.assertTrue(any("missing.md" in error for error in errors))
            (root / "docs/guide.md").write_text(SOURCE + "\nChanged.\n", encoding="utf-8")
            self.assertTrue(any("source hash drift" in error for error in validate_tree(root)[0]))

    def test_uninventoried_mirror_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_tree(root)
            (root / "docs/i18n/es/docs/extra.md").write_text("# Extra\n", encoding="utf-8")
            self.assertTrue(any("uninventoried" in error for error in validate_tree(root)[0]))

    def test_pending_is_not_claimed_as_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_tree(root)
            path = root / "docs/i18n/manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            record = manifest["sources"][0]["mirrors"]["es"]
            record["status"] = "pending"
            record.pop("source_sha256")
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("pending mirror exists" in error for error in validate_tree(root)[0]))


if __name__ == "__main__":
    unittest.main()
