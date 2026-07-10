# README Information Architecture Design

## Goal

Make Harneloop understandable to non-technical users, useful as an operating guide for agents, and easy to navigate for technical readers.

## Approach

Use progressive disclosure rather than separate audience-specific READMEs:

1. Define Harneloop in plain language and state what it is not.
2. Provide navigation for agents, users, and technical readers.
3. Explain the problem, harness units, and lifecycle before installation details.
4. Give agents a direct onboarding contract and a reusable natural-language starter prompt.
5. Explain environment mapping, configuration, use cases, CLI commands, and integrity guarantees with increasing technical depth.

This keeps one canonical entry point for people and repository-reading agents while linking specialized architecture documents for deeper detail.

## Visual

The framework-process Mermaid graph flows from top to bottom so the attempt, artifact, diagnosis, candidate, evidence, and promotion sequence reads naturally on documentation pages and can guide a later designed image.

## Validation

- Verify every README link resolves to an existing repository file.
- Verify documented commands and preference keys against the current CLI and source.
- Run the full test suite, compile check, diagnostics, and `git diff --check`.
