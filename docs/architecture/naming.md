# Naming Notes

## Current Term

The current portable harness object is called a **harness unit** in docs and commands.

This name is serviceable for the prototype because it is neutral, generic, and accurate: it describes one self-contained harness workspace with control files, agent-facing instructions, candidates, versions, environment contracts, runtime records, and exports.

## Concern

`unit` is also bland and not very memorable. It works as an internal technical term, but it may not be the best user-facing product noun if EvoRig becomes public.

## Candidate Direction

Use this distinction unless we decide to rename:

- **Harness unit**: precise internal/framework term.
- **Rig**: possible user-facing term, especially if the project name remains EvoRig.

Example:

- User-facing: "Create a rig", "list rigs", "export this rig".
- Internal/docs: "A rig is stored as a harness unit directory."

## Tradeoffs

`Rig` has stronger identity and matches EvoRig, but it can sound Blender-specific because rigging is common in 3D workflows. That is the main reason not to rename immediately.

`Harness` is clearer and less branded, but more generic.

`Unit` is stable and neutral, but less marketable.

## Recommendation

Keep `unit` in the code for now. During real testing, listen for whether users naturally say "unit", "harness", or "rig". If EvoRig remains the product name, consider changing the human CLI labels to "rig" first while keeping `unit` as a backward-compatible command alias.
