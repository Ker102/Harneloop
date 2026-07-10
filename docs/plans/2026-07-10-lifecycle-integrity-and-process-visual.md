# Lifecycle Integrity And Process Visual

## Goal

Close the run-mutation and stale-evidence gaps found during the ViperMesh case study, then add a clear repo-native visual of the Harneloop process.

## Design

- A run accepts artifacts only while its status is `running`.
- The first successful `run finish` transition is terminal and cannot be overwritten.
- Narrative evidence may stand alone, but every declared run, artifact, and file reference must exist when evidence is added.
- Promotion revalidates evidence references so deleted or stale evidence cannot pass the gate.
- The process visual uses Mermaid so GitHub can render it directly and the same source can guide a later polished image.

## Validation

- Add regression tests before implementation.
- Run the full unittest suite and compile check.
- Run `harneloop doctor`, CLI smoke checks, and `git diff --check`.
