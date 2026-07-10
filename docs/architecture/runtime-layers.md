# Runtime Layers

## Current Decision

Use Python for the first reference implementation.

Prefer Rust over Go later if Harneloop needs a native protected runtime.

## Why Rust Later

The native layer should exist only if the framework needs stronger local guarantees around:

- lifecycle integrity;
- protected state boundaries;
- version snapshots;
- rollback;
- content-addressed storage;
- artifact packaging;
- file watching;
- subprocess supervision;
- desktop packaging.

Rust fits that protected-kernel role better than Go for this product shape.

## Agent Boundary

Rust should not become the agent's open-ended harness-design workspace.

Agents should continue to work through:

- Markdown instructions;
- YAML and JSON manifests;
- schemas;
- candidate directories;
- CLI commands;
- artifact contracts.

The rule remains:

> Agents can explore freely inside candidates. The engine controls promotion.

## Where Go Could Still Fit

Go remains a good candidate for future hosted services, remote worker coordination, or registry infrastructure if Harneloop grows in that direction.
