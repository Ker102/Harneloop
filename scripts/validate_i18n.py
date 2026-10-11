"""Validate documentation mirrors without dependencies or application changes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")
REFERENCE = re.compile(r"^ {0,3}\[([^]]+)\]:\s*<?([^\s>]+)>?", re.MULTILINE)


def slug(text: str) -> str:
    text = re.sub(r"<[^>]*>", "", text)
    text = text.replace("`", "").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def split_code(text: str) -> tuple[str, list[str], list[str]]:
    prose: list[str] = []
    blocks: list[str] = []
    errors: list[str] = []
    current: list[str] | None = None
    delimiter = ""
    for line in text.replace("\r\n", "\n").splitlines():
        match = FENCE.match(line)
        if current is None:
            if match:
                delimiter = match[1]
                current = [line]
                prose.append("")
            else:
                prose.append(line)
        else:
            current.append(line)
            if match and match[1][0] == delimiter[0] and len(match[1]) >= len(delimiter) and not match[2].strip():
                blocks.append("\n".join(current))
                current = None
    if current is not None:
        errors.append("unclosed code fence")
    return "\n".join(prose), blocks, errors


class HtmlReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is None:
                continue
            if key in {"href", "src"}:
                self.links.append(value)
            if key == "id" or (tag == "a" and key == "name"):
                self.ids.add(value)


def references(prose: str) -> list[str]:
    html = HtmlReferences()
    html.feed(prose)
    # Inline code is literal documentation, not a Markdown link destination.
    plain = INLINE_CODE.sub("", prose)
    return html.links + [match[1].strip("<>") for match in MARKDOWN_LINK.finditer(plain)] + [match[2] for match in REFERENCE.finditer(plain)]


def anchors(text: str) -> set[str]:
    prose, _, _ = split_code(text)
    html = HtmlReferences()
    html.feed(prose)
    result = set(html.ids)
    seen: Counter[str] = Counter()
    for match in re.finditer(r"^#{1,6}\s+(.+)$", prose, re.MULTILINE):
        base = slug(match[1])
        count = seen[base]
        result.add(base if count == 0 else f"{base}-{count}")
        seen[base] += 1
    return result


def strip_navigation(text: str) -> str:
    return re.sub(r"<!-- i18n-switcher:start -->.*?<!-- i18n-switcher:end -->\s*", "", text, flags=re.DOTALL)


def structure(prose: str) -> tuple[list[int], int, int, int]:
    prose = re.sub(r'^<a id="[^"]+"></a>\n?', "", prose, flags=re.MULTILINE)
    headings = [len(match[1]) for match in re.finditer(r"^(#{1,6})\s", prose, re.MULTILINE)]
    lists = len(re.findall(r"^\s*(?:[-*+] |\d+\. )", prose, re.MULTILINE))
    tables = len(re.findall(r"^\|", prose, re.MULTILINE))
    paragraphs = len([part for part in re.split(r"\n\s*\n", prose.strip()) if part.strip()])
    return headings, lists, tables, paragraphs


def compare_documents(source: str, mirror: str) -> list[str]:
    source, mirror = strip_navigation(source), strip_navigation(mirror)
    original, original_blocks, errors = split_code(source)
    translated, translated_blocks, mirror_errors = split_code(mirror)
    errors += mirror_errors
    if original_blocks != translated_blocks:
        errors.append("fenced code differs from English source")
    if INLINE_CODE.findall(original) != INLINE_CODE.findall(translated):
        errors.append("inline code differs from English source")
    if structure(original) != structure(translated):
        errors.append("document structure differs (headings, lists, tables, or prose blocks)")
    external = lambda text: Counter(link for link in references(text) if urlsplit(link).scheme or link.startswith("//"))
    if external(original) != external(translated):
        errors.append("external URLs differ from English source")
    return errors


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes repository: {relative}")
    return path


def link_errors(root: Path, path: Path, text: str) -> list[str]:
    prose, _, _ = split_code(text)
    errors: list[str] = []
    for link in references(prose):
        url = urlsplit(link)
        if url.scheme or link.startswith("//"):
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(root.resolve()):
            errors.append(f"link escapes repository: {link}")
        elif not target.exists():
            errors.append(f"broken link: {link}")
        elif url.fragment and target.suffix.lower() == ".md":
            if unquote(url.fragment) not in anchors(target.read_text(encoding="utf-8")):
                errors.append(f"broken fragment: {link}")
    return errors


def maintained_sources(root: Path) -> set[str]:
    paths = [root / name for name in ("README.md", "CONTRIBUTING.md", "SECURITY.md")]
    paths += list((root / "docs").glob("*.md")) + list((root / "docs/architecture").glob("*.md"))
    return {path.relative_to(root).as_posix() for path in paths if path.exists()}


def source_hash(path: Path) -> str:
    # Hash repository content consistently across Windows and Linux checkouts.
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate_tree(root: Path) -> tuple[list[str], dict[str, tuple[int, int]]]:
    root = root.resolve()
    manifest = json.loads((root / "docs/i18n/manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    locales = manifest["locales"]
    if manifest.get("schema_version") != 1 or len(set(locales)) != len(locales):
        errors.append("invalid manifest schema or duplicate locales")
    sources = manifest["sources"]
    paths = [source["path"] for source in sources]
    if len(set(paths)) != len(paths):
        errors.append("duplicate source paths")
    if set(paths) != maintained_sources(root):
        errors.append("maintained source inventory differs from manifest")
    counts = dict.fromkeys(locales, 0)
    declared: set[str] = set()
    for record in sources:
        source_path = contained(root, record["path"])
        if not source_path.is_file():
            errors.append(f"missing source: {record['path']}")
            continue
        digest = source_hash(source_path)
        if digest != record["sha256"]:
            errors.append(f"source hash drift: {record['path']}")
        source_text = source_path.read_text(encoding="utf-8")
        if set(record["mirrors"]) != set(locales):
            errors.append(f"missing or unknown locale entries: {record['path']}")
        for locale in locales:
            mirror = record["mirrors"].get(locale)
            if mirror is None:
                continue
            expected = f"docs/i18n/{locale}/{record['path']}"
            if mirror["path"] != expected:
                errors.append(f"incorrect mirror path: {mirror['path']}")
                continue
            path = contained(root, expected)
            declared.add(expected)
            if mirror["status"] == "pending":
                if path.exists():
                    errors.append(f"pending mirror exists: {expected}")
                continue
            if mirror["status"] != "complete":
                errors.append(f"unknown mirror status: {expected}")
                continue
            if mirror.get("source_sha256") != digest:
                errors.append(f"stale mirror source hash: {expected}")
            if not path.is_file():
                errors.append(f"missing completed mirror: {expected}")
                continue
            counts[locale] += 1
            text = path.read_text(encoding="utf-8")
            errors += [f"{expected}: {error}" for error in compare_documents(source_text, text)]
            errors += [f"{expected}: {error}" for error in link_errors(root, path, text)]
    for locale in locales:
        for path in (root / "docs/i18n" / locale).rglob("*.md"):
            if path.relative_to(root).as_posix() not in declared:
                errors.append(f"uninventoried mirror: {path.relative_to(root).as_posix()}")
    for relative in ("README.md", "docs/i18n/README.md"):
        path = root / relative
        if path.is_file():
            errors += [f"{relative}: {error}" for error in link_errors(root, path, path.read_text(encoding="utf-8"))]
    return errors, {locale: (count, len(sources)) for locale, count in counts.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true", help="also fail on pending mirrors")
    args = parser.parse_args()
    try:
        errors, counts = validate_tree(Path(__file__).resolve().parents[1])
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1
    for locale, (count, total) in counts.items():
        print(f"{locale}: {count}/{total} complete, {total - count} pending")
        if args.require_complete and count != total:
            errors.append(f"{locale}: incomplete coverage")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Validation {'FAILED' if errors else 'PASSED'} ({len(errors)} errors)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
