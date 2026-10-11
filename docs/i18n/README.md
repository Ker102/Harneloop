# Documentation Translations

English is authoritative. Translate from the current English file, not another
translation. If wording conflicts, follow English and report the discrepancy.
The canonical repository is [Ker102/Harneloop](https://github.com/Ker102/Harneloop).

## Languages And Coverage

| Locale | Language | Completed maintained documents |
|---|---|---|
| `es` | [Español](es/README.md) | 14/14 |
| `zh-CN` | [简体中文](zh-CN/README.md) | 14/14 |
| `fr` | [Français](fr/README.md) | 14/14 |
| `ja` | [日本語](ja/README.md) | 14/14 |
| `de` | [Deutsch](de/README.md) | 14/14 |
| `pt-BR` | [Português (Brasil)](pt-BR/README.md) | 14/14 |

The [manifest](manifest.json) is the explicit inventory: source paths, SHA-256
hashes, requested locales, completed mirror paths, and the source hash reviewed
for each mirror. There are 84 complete mirrors and no pending maintained files
in this snapshot. These translations were drafted and reviewed by the coding
agent for fidelity, not independently certified by native-speaking reviewers.

## Scope

Included: the full root README, CONTRIBUTING and SECURITY, all maintained
Markdown files directly in `docs/`, and all `docs/architecture/*.md` references.
Every mirror uses `docs/i18n/<locale>/<repo-relative-source-path>`, for example
`docs/i18n/es/docs/agent-onboarding.md`. The inventory does not claim to translate
the software interface or every file in the repository.

Historical release notes [v0.0.1](../releases/v0.0.1.md) and
[v0.0.2](../releases/v0.0.2.md) remain untranslated English history. Internal
plans, task/progress records, AGENTS/CLAUDE instructions, executable agent skills,
GitHub templates, generated run records, private/local evidence, and vendor
documentation are excluded. LICENSE remains the authoritative English legal
text. Assets and raw Mermaid diagram sources remain shared originals.

## Fidelity And Links

Translate the whole document, preserving its sections, lists, tables, examples,
numbers, API names, safety limitations, and public-alpha caveats. Do not replace
it with a summary or strengthen claims. Fenced code (including prompts, diagrams,
directory trees, English comments, and example string values) and inline code
are deliberately unchanged. External URLs remain unchanged.

Internal documentation links point to completed mirrors in the same locale;
shared assets, LICENSE, and excluded materials point back to the originals.
Explicit English heading anchors keep the original fragment links working even
when headings are translated. The README language switchers use relative links.

## Maintenance

1. Edit the authoritative English source first.
2. Run `python scripts/validate_i18n.py` from the repository root. It reports
   coverage and rejects changed source hashes, stale or missing complete mirrors,
   uninventoried files, broken local Markdown/HTML links and heading fragments,
   unclosed/changed fences, changed inline code or external URLs, and mismatched
   section/list/table/prose-block structure.
3. Review and update every affected translation. Check factual equivalence,
   especially permissions, negations, alpha limits, results and evaluation scope.
   The validator is a structural safeguard, not a semantic or fluency evaluator.
4. Only after review, compute the source's SHA-256 and update its `sha256` and
   each completed mirror's `source_sha256` in the manifest. Hashes cover the
   UTF-8 source bytes with CRLF normalized to LF, including the README switcher.
   All other bytes are significant; keep the repository's LF line endings.
   Never refresh hashes just to silence stale detection.
5. If a mirror is not complete, mark it `pending`, omit `source_sha256`, and do
   not leave a partial file at its completed mirror path. Update the coverage
   table and document the gap. Do not claim full coverage until it is complete.
6. For a newly maintained source, add it and all six locale entries to the
   manifest, translate it fully, and rewrite the relevant links. If documentation
   is reorganized into new directories, update the validator's inventory scope
   deliberately rather than silently omitting those files.
7. Run `python scripts/validate_i18n.py --require-complete` and
   `python -m unittest discover -s tests`. The existing test discovery includes a
   real-repository translation validation test; no separate CI workflow is needed.

The checker uses only the project's standard Python runtime and standard library.
It validates local links without contacting external services. It recognizes the
inline, reference-definition, and HTML link forms used by these sources; it is not
a complete Markdown renderer and does not verify remote pages or natural-language
claims. Review new Markdown syntax when adding it. A passing check alone does not
establish translation accuracy.
