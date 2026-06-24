# EvoRig

Temporary working name.

EvoRig is a protocol-first framework for building self-evolving agent harnesses. The first goal is not to build another eval dashboard. The goal is to give agents a structured way to attempt artifact-producing tasks, inspect what actually happened, trace failures, propose candidate harness changes, test those changes, and promote only evidence-backed improvements.

The name may change before public launch. The architecture should not depend on the name.

## Current Core

This repository starts with the generic lifecycle engine:

- create portable harness units;
- create candidate harness patches;
- keep agents inside candidate sandboxes;
- protect framework-owned control files;
- promote candidates into restorable version snapshots;
- roll back to prior snapshots;
- package thin units;
- record explicit wait, stop, and resume state.

The first demo may use Blender, but the framework core must stay task-family-neutral.

## Development Status

Private prototype. API and file formats are expected to change.

## Quick Start

```powershell
python -m evorig init-unit .\demo-unit --id demo-unit --name "Demo Unit"
python -m evorig candidate create .\demo-unit --summary "Add first task principle"
python -m evorig status .\demo-unit
```

Run tests:

```powershell
python -m unittest discover -s tests
```
