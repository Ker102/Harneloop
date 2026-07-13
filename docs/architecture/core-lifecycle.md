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

## Candidates

A candidate is a coherent change batch or hypothesis, not one file edit or Git commit. Related setup, tool, instruction, or validator changes may accumulate in one candidate when they should be tested and promoted together. Agents may keep multiple candidates open when they address independent problems, such as a target-harness improvement and a separate evaluation repair.

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

Each current candidate declares:

- an impact plane: `target_harness`, `evaluation`, `infrastructure`, or `mixed`;
- a validation tier: `structural`, `targeted`, `representative`, or `full`;
- a lifecycle stage: `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted`, or `rejected`;
- the promoted harness version on which it is based.

Validation is proportional to risk. Structural checks fit metadata-only changes. Targeted checks fit isolated infrastructure or evaluator repairs. Representative runs fit behavior-changing harness work. Full regression suites are reserved for broad changes and release checkpoints. An agent can choose a stronger tier, but should not rerun the entire artifact benchmark for every incremental setup edit.

Evaluation changes and target-harness changes should normally remain separate candidates so a changed judge cannot be used as the sole proof that a changed harness improved. A candidate may remain `accumulating` while related work is batched, then move to `ready` once it is coherent enough to validate.

## Promotion

Promotion applies one ready candidate overlay to the harness unit, creates a restorable snapshot under `versions/`, and updates provenance. Promoted versions remain linear even when candidate work is parallel.

If two open candidates share the same base, promoting one marks the other `needs_rebase`. Its files and history remain intact, but it must be reconciled with the new version and collect fresh evidence before promotion. Previous evidence remains provenance and cannot satisfy the new base-version gate.

Evidence references are integrity-checked when they are attached and again at promotion. A declared run and artifact must exist, the artifact's stored file must still be present, and any directly referenced evidence file must exist. Narrative evidence may omit these references.

## Run Integrity

A run is mutable only while its status is `running`. Artifacts can be attached during that phase. The first successful `run finish` transition is terminal: later artifact additions and repeated finish attempts are rejected so the original result cannot be silently rewritten.

## Rollback

Rollback restores a prior promoted snapshot. It should be a framework action with provenance, not a manual copy.

## Wait And Stop

The runtime lifecycle supports explicit waiting and stopping.

Waiting covers delayed artifacts, human review, queued jobs, cooldowns, and infrastructure rebuilds.

Stopping covers sufficient evidence, plateau, capability frontier concerns, permission needs, or cases where the next useful step depends on a human or external system.

See [How Harneloop Works](../framework-process.md) for the full artifact-aware evolution loop.
