# Core Lifecycle

## Unit

A harness unit is a portable directory that contains reusable harness material and framework control files.

Required files:

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  candidates/
  versions/
  provenance/
```

Common optional folders:

```text
agent-facing/
observers/
validators/
regression-cases/
infrastructure/
exports/
tools/
memory/
experiments/
```

## Candidate

A candidate is a concrete patch object. Agents may create files, notes, research, helper tools, observers, validators, and proposed instructions inside the candidate workspace.

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

Candidate changes are applied through the framework. Candidate overlays cannot edit protected paths such as `unit.yaml`, `versions/`, `provenance/`, `.evolve/`, or `candidates/`.

## Promotion

Promotion applies a candidate overlay to the unit, creates a restorable snapshot under `versions/`, updates provenance, and clears the active candidate.

## Rollback

Rollback restores a prior promoted snapshot. It should be a framework action with provenance, not a manual copy.

## Wait And Stop

The runtime lifecycle supports explicit waiting and stopping.

Waiting covers delayed artifacts, human review, queued jobs, cooldowns, and infrastructure rebuilds.

Stopping covers sufficient evidence, plateau, capability frontier concerns, permission needs, or cases where the next useful step depends on a human or external system.
