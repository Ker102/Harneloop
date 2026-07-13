---
name: evolving-harnesses-with-harneloop
description: Operates Harneloop harness units through adaptive intake, environment mapping, artifact-aware attempts, explicit evaluation decisions, candidates, and evidence-gated promotion. Use when creating, continuing, evaluating, or recovering context for a Harneloop harness unit.
---

# Evolving Harnesses With Harneloop

Apply this protocol only to work involving the active harness unit. Do not treat unrelated work in the same conversation as Harneloop work.

## Enter Or Resume A Unit

1. Run `harneloop brief <unit>`.
2. Read `<unit>/AGENTS.md`, `<unit>/UNIT_AGENT.md`, and `<unit>/operational-map.md`.
3. Follow the recorded next action unless current evidence invalidates it.

## Reconcile Intake

Scaffold and inspect before asking generic questions. Run `harneloop intake status <unit>` and distinguish user-confirmed facts, delegated decisions, inferences, and unknowns.

Ask only unresolved questions that can materially change the target, environment, evidence, permissions, or success judgment. Do not silently turn an inference into confirmed unit context. Before the first run, resolve relevant fields and record user confirmation or delegation with `harneloop intake acknowledge`.

## Close Every Attempt

1. Plan the attempt and expected artifacts.
2. Start a run, perform the real task, and attach useful artifacts.
3. Finish the run. Execution success means the task ran; it does not prove result quality.
4. Inspect the artifacts and add observations.
5. Run `harneloop attempt conclude` with one decision:
   - `accept`: evidence passes and no candidate is justified.
   - `create_candidate`: a harness change should be tested.
   - `rerun`: the attempt or evidence plan needs correction first.
   - `request_input`: missing user or external input blocks a sound judgment.
   - `stop`: further work is not currently justified.

Never stop immediately after task execution. Record the evaluation and decision even when the first result is already good enough.

## Develop Changes

Keep proposed harness changes inside a candidate. Reuse suitable existing tools and prior work when useful. Test against the target and relevant regressions, attach run-linked evidence, and promote only when improvement is supported.

## Recover From Context Loss

Run `harneloop brief <unit>` again. The framework-managed brief is the compact source for the active target, intake state, latest evaluation decision, and next action.
