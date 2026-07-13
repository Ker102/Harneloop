# Adaptive Intake And Loop Closure Design

## Goal

Prevent agents from silently turning assumptions into harness-unit truth, require every completed attempt to end in an explicit evidence-backed decision, and preserve unit context without claiming the user's entire agent session.

## Architecture

Harneloop will add a framework-owned intake record that classifies important context as confirmed, delegated, inferred, unknown, or not applicable. The default adaptive policy allows reversible scaffolding and environment inspection, then requires a concise checkpoint before the first run when high-impact context remains unresolved.

Runs continue to describe execution. Attempt conclusions separately record result quality, artifact coverage, confidence, and the next lifecycle decision: accept the current harness, create a candidate, rerun, request input, or stop. Finishing a run moves the unit to `awaiting_evaluation`; it no longer implies that the artifact itself succeeded.

Every unit receives a compact, framework-managed session brief and a thin unit-local `AGENTS.md`. Both are scoped with “when working on this harness unit” language, so unrelated work in the same agent session remains unaffected. A `harneloop brief` command provides context recovery after compaction. A bundled skill documents the complete operating protocol but does not replace engine state or gates.

## Data Flow

1. Initialize unit and provisional intake record.
2. Inspect the environment and update intake facts.
3. Surface unresolved high-impact questions or record explicit user delegation.
4. Plan and run the task; capture artifacts.
5. Finish execution and enter `awaiting_evaluation`.
6. Conclude the attempt with outcome, artifact coverage, confidence, and decision.
7. Follow the concrete decision: accept, create candidate, rerun, wait for input, or stop.

## Boundaries

- Questions remain adaptive rather than a mandatory generic questionnaire.
- A user may explicitly delegate decisions to the agent.
- Inferred context stays visibly provisional.
- Missing evidence can produce a partial or inconclusive conclusion, but not an unqualified pass.
- The unit-local rule applies only when work concerns that unit.
- Target-workspace adapters remain optional because modifying another project requires an explicit action.

## Testing

- New units contain intake, scoped agent instructions, and a session brief.
- A first run is blocked until adaptive intake has been acknowledged through confirmation or delegation.
- Finishing a run produces `awaiting_evaluation`.
- Conclusions detect missing expected artifact kinds.
- `accept` records that no candidate is needed.
- `request_input` enters a resumable wait state with a concrete user question.
- `harneloop brief` prints objective, state, assumptions, evidence status, and next action.
