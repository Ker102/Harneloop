# Development

## Repository Layout

```text
src/evorig/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

## Local Verification

```powershell
.\.venv\Scripts\python -m compileall src tests
.\.venv\Scripts\python -m unittest discover -s tests
.\.venv\Scripts\evorig doctor
```

## DevOps Baseline

The repository should maintain:

- source layout with `src/`;
- repeatable local tests;
- CI for supported Python versions;
- no checked-in virtual environments or runtime artifacts;
- explicit security and contribution docs;
- language-neutral schemas for core records.

## Runtime Data

Runtime traces, copied artifacts, and run records are local working data. They live under unit-local `runtime/` directories and should not be promoted into portable packages unless a later packaging profile explicitly includes them.

## PR Review Note

CodeRabbit review is not needed during the early prototype. If a PR is created, add the configured CodeRabbit-ignore tag or label.
