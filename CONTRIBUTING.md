# Contributing

Harneloop is currently a public alpha. Focused issues and contributions are welcome while the public API and harness-unit formats stabilize.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

On macOS or Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

## Pull Requests

Keep pull requests scoped to one behavior or architectural slice.

Open an issue before substantial architectural work so the problem and compatibility impact can be agreed on first. Include tests for lifecycle changes and update agent-facing documentation when behavior changes.

For now, do not request automated CodeRabbit review. If a PR is created while CodeRabbit is configured, add the repository's CodeRabbit-ignore label or tag before requesting review.

## Standards

- Keep the framework core task-family-neutral.
- Do not add Blender-specific assumptions to `src/harneloop`.
- Add or update tests for lifecycle behavior.
- Keep agent-facing files readable in Markdown, YAML, or JSON.
- Do not commit secrets, local runtime artifacts, virtual environments, or generated packages.

By contributing, you agree that your contribution is licensed under the repository's [Apache License 2.0](LICENSE).
