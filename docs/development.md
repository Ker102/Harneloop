# Development

## Repository Layout

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

## Local Verification

```powershell
.\.venv\Scripts\python -m compileall src tests
.\.venv\Scripts\python -m unittest discover -s tests
.\.venv\Scripts\harneloop doctor
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

Runtime traces, copied artifacts, run records, attempt plans, and experiments are local working data. They should not be promoted into thin portable packages unless a later packaging profile explicitly includes them.

## PR Review Note

CodeRabbit review is not needed during the early prototype. If a PR is created, add the configured CodeRabbit-ignore tag or label.
