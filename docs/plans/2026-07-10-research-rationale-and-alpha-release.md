# Research Rationale And Alpha Release

## Goal

Explain why EvoRig treats the harness as the first task-specific optimization surface and publish the current implementation as the `v0.0.1` private alpha.

## Documentation Approach

- State the harness-first position strongly but avoid a universal comparison unsupported by research.
- Link directly to primary papers covering self-improving harnesses, agent-computer interfaces, iterative feedback, retrieval versus fine-tuning, and fine-tuning risks.
- Distinguish research support from the origin of EvoRig: the project came from practical agent-development experience, while the papers independently support its direction.
- Document where fine-tuning remains useful and that harness improvements can complement it.

## Release

- Tag the current package version as `v0.0.1`.
- Publish it as a GitHub prerelease titled `EvoRig v0.0.1 - Private Alpha`.
- Include capabilities, current boundaries, and source-install instructions.

## Validation

- Check README and release-note links.
- Run the full test suite, compile check, diagnostics, and `git diff --check`.
- Confirm the tag and GitHub release resolve to the committed alpha state.
