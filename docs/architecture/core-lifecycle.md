# Core Lifecycle

## Harness Unit

A harness unit is a portable directory that contains reusable harness material and framework control files.

Required files:

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` is the unit-local orientation document. It records the agent's current understanding of what the harness unit improves, how the target environment is used, what artifacts or evidence are useful, how runs and resets usually happen, operating-agent capability gaps, unit/target-agent tools, known fragile spots, assumptions, open questions, and where prior evidence lives. It should guide the agent without becoming a rigid procedure.

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

Promotion applies a candidate overlay to the harness unit, creates a restorable snapshot under `versions/`, updates provenance, and clears the active candidate.

Evidence references are integrity-checked when they are attached and again at promotion. A declared run and artifact must exist, the artifact's stored file must still be present, and any directly referenced evidence file must exist. Narrative evidence may omit these references.

## Run Integrity

A run is mutable only while its status is `running`. Artifacts can be attached during that phase. The first successful `run finish` transition is terminal: later artifact additions and repeated finish attempts are rejected so the original result cannot be silently rewritten.

## Rollback

Rollback restores a prior promoted snapshot. It should be a framework action with provenance, not a manual copy.

## Wait And Stop

The runtime lifecycle supports explicit waiting and stopping.

Waiting covers delayed artifacts, human review, queued jobs, cooldowns, and infrastructure rebuilds.

Stopping covers sufficient evidence, plateau, capability frontier concerns, permission needs, or cases where the next useful step depends on a human or external system.

See [How EvoRig Works](../framework-process.md) for the full artifact-aware evolution loop.
