# Capability Gaps For Operating Agents

Status: implemented.

## Goal

EvoRig should not assume the agent building a harness unit has full Codex-like capabilities.

Some operating agents may lack terminal access, filesystem access, browser access, package managers, MCP servers, visual inspection, database access, network access, or custom project tools. Missing capabilities can reduce harness-building quality, especially for artifact-aware tasks.

## Architecture

Track two separate layers:

- Operating-agent capabilities: what the current agent can actually use while building and testing the harness unit.
- Unit/target-agent tools: tools designed into the harness unit or provided to the target agent through the environment contract.

The generated `operational-map.md` includes a `Capability Gaps` section for:

- current available operating-agent capabilities;
- missing operating-agent capabilities;
- unit or target-agent tools;
- requested or enabled tools;
- risk, cost, auth, and security notes;
- fallbacks if the user declines.

## Permission Boundary

Low-risk local capabilities can be installed, enabled, or built when the environment allows it.

Larger dependencies, credentials, paid APIs, user-owned accounts, external access, network expansion, or security-impacting changes should be proposed first.

Capability additions should be justified by observed bottlenecks, failed attempts, missing artifacts, or clear expected improvement, not added speculatively.

## Validation

- Add tests that generated operational maps include capability-gap tracking.
- Add tests that `evorig onboard` explains operating-agent capabilities, unit/target-agent tools, and evidence-backed capability additions.
