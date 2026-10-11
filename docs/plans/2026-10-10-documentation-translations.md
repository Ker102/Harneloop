# Documentation Translation Implementation Plan

> For Agent: Use executing-plans to implement this documentation-only plan.

**Goal:** Equivalent maintained public documentation in es, zh-CN, fr, ja, de, and pt-BR, with honest inventory and local checks.

**Architecture:** Mirror repository-relative Markdown paths below docs/i18n/<locale>/. English remains authoritative. Preserve code and external URLs; redirect internal documentation to completed locale mirrors and other repository resources to English originals. Explicit English heading anchors preserve fragment navigation.

**Tech Stack:** Existing Python standard library and unittest. No application runtime changes or added dependencies.

## Ordered Work

1. Inventory README.md, CONTRIBUTING.md, SECURITY.md, maintained docs/*.md and docs/architecture/*.md. Exclude agent instruction files, plans, historical releases, templates, executable skills, assets, and private/generated evidence. Record hashes and pending locale entries in docs/i18n/manifest.json.
2. Add scripts/validate_i18n.py and tests/test_i18n.py. Test broken links, fragments, altered/unclosed fences, inline-code changes, omitted sections, source drift, and dishonest completion before trusting the checker.
3. Translate the full README and maintained contributor/security/guides/reference files. Create complete mirrors only; do not substitute summaries or mark partial translations complete.
4. Add compact native-language switchers to the authoritative README and locale READMEs, plus docs/i18n/README.md maintenance instructions and explicit remaining coverage.
5. Review wording for factual drift, validate all mirrors, run the existing suite, and inspect git diff/status. Do not stage, commit, or push.

## Validation And Checkpoints

- Use python -m unittest discover -s tests -p test_i18n.py for the focused validator tests.
- Use python scripts/validate_i18n.py for coverage, link, structure, code, and hash checks.
- Use python -m unittest discover -s tests for regression verification.
- Record pending maintained files explicitly rather than treating omitted sources as out of scope.
- Preserve the existing untracked .playwright-cli/ directory.

## Progress

- [x] Read inherited instructions, inspect nested git status and Python project conventions.
- [x] Inventory, validator, and focused tests.
- [x] Complete locale mirrors and navigation.
- [x] Fidelity review and final validation.

## Verified Outcome

- 14 maintained sources mirrored fully in each of six locales (84 mirrors).
- No pending maintained sources. Historical releases and the explicit excluded
  categories remain English originals, not claimed as translated.
- Strict validator: 0 errors. Focused validator suite: 12 tests passed.
- Full suite: 62 tests passed using .venv/Scripts/python.exe. The system Python
  lacks the installed harneloop package, so it cannot run the application suite.
- Existing CI unittest discovery now includes a real-repository inventory/hash/
  mirror validation test and requires complete maintained coverage.
- Source hashes normalize CRLF to LF for Windows/Linux checkout consistency;
  all other source bytes remain significant. Code blocks and inline code match.
- Temporary translation drafts removed. Application sources, dependencies,
  workflows, user evidence, and git index were not changed. No commit or push.
- Semantic fidelity reviewed by the coding agent; independent native-speaker
  review remains a useful quality assurance step, not completed certification.

## Publication Checkpoint

On 2026-10-11 Kristofer authorized committing and pushing the reviewed translation
batch. Unrelated browser artifacts remain local. Validation passed again before
staging; no application sources or dependencies are included in this commit.
