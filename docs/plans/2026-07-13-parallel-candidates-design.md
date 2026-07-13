# Parallel Candidates And Scaled Validation Design

## Goal

Let an agent accumulate and validate several coherent harness-change candidates at once without requiring a full artifact benchmark for every implementation commit.

## Design Principles

- A candidate is a coherent change batch and hypothesis, not a single commit.
- Several candidates may be open concurrently when they solve different problems.
- Validation cost should match the candidate's impact and risk.
- Evaluation changes must remain distinguishable from target-harness changes so an agent cannot improve its result by silently changing the measurement system.
- Promotion remains evidence-gated and produces one linear, restorable harness-unit version history.

## Candidate Model

Every new candidate records:

- `plane`: `target_harness`, `evaluation`, `infrastructure`, or `mixed`;
- `validation_tier`: `structural`, `targeted`, `representative`, or `full`;
- `status`: `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted`, or `rejected`;
- `base_version`: the promoted harness version against which it is being developed;
- an overlay containing any number of related unit-local changes;
- evidence records tied to the candidate base version and validation tier.

The agent can keep a candidate in `accumulating` while adding related changes and running inexpensive checks. It marks the batch `ready` when the objective is coherent and the intended validation is complete enough for promotion. A secondary candidate can be created at any time, such as an evaluation fix discovered while a target-harness tool candidate is still accumulating.

## Validation Tiers

- `structural`: schemas, deterministic fixtures, static checks, or contract validation.
- `targeted`: focused smoke tests or one narrow real workflow.
- `representative`: artifact-producing tasks representative of intended use plus relevant regressions.
- `full`: the broad benchmark or release suite.

Evidence records declare the tier they establish. Promotion requires supporting evidence at or above the candidate's required tier. Representative and full evidence must point to a recorded run. Full validation is reserved for high-impact changes and release checkpoints rather than every helper or tool commit.

## Parallel Promotion And Rebase

Promoted versions remain linear. If candidate A and candidate B share base version `0.2.0`, promoting A creates `0.3.0` and marks B `needs_rebase`. B remains available, but it cannot be promoted until the agent reconciles it with `0.3.0`, runs `candidate rebase`, and records fresh evidence for the new base. Older evidence remains in provenance but does not satisfy the new promotion gate.

## State And Agent Context

Unit state records `active_candidates` while retaining `active_candidate` as a compatibility and focus hint. Allowed-edit guidance includes every open candidate workspace. Status and brief output summarize all candidates so context recovery does not hide parallel work.

## Compatibility

Existing candidates without the new schema retain legacy promotion behavior. Existing units gain `active_candidates` lazily when a candidate command next updates state. No promoted snapshots or runtime evidence are rewritten.

## Testing Strategy

- Create two candidates and verify both remain active and editable.
- Promote one and verify the other becomes `needs_rebase`.
- Reject stale promotion, then rebase and require fresh evidence.
- Verify structural evidence can be file-based and representative/full evidence requires a run.
- Verify candidate list/status and unit brief expose parallel state.
- Preserve existing lifecycle, locking, packaging, rollback, and legacy-candidate tests.
