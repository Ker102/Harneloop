# Concurrency And File Safety

Harneloop commands may be launched by agents in quick succession or in parallel. Any command that reads a control file, computes a sequential ID, and writes the file back must protect that whole read-modify-write section.

## Current Rule

- Use a harness-unit lock file for shared lifecycle sections.
- Reread the relevant YAML or JSON file inside the lock.
- Allocate the next sequential ID inside the lock.
- Write YAML and JSON through atomic temp-file replacement.
- Release the lock only after the file update is complete.

## Implemented Locks

- `runs`: allocates run IDs.
- `run-<id>`: adds artifacts and finishes a run.
- `attempts`: allocates attempt IDs.
- `attempt-<id>`: appends attempt observations.
- `candidates`: allocates candidate IDs.
- `candidate-<id>-evidence`: allocates evidence IDs.
- `lifecycle`: promotes candidates and rolls back versions.
- `state`: updates `.evolve/state.json` and derived state files.

Locks live under `.evolve/locks/`, which is framework-owned runtime state and excluded from portable packages.

## Rust Runtime Note

This does not require Rust yet. Python file locks and atomic replace are sufficient for the alpha CLI. A future Rust runtime can own stricter sandboxing, process supervision, and higher-confidence concurrent file coordination once the product surface stabilizes.
