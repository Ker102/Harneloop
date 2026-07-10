# Naming

## Selected Term

The portable harness object is called a **harness unit**.

A harness unit is one self-contained Harneloop workspace with control files, agent-facing instructions, candidates, versions, environment contracts, runtime records, and exports.

## Why This Name

`Harness unit` is clearer than `unit` because it keeps the purpose visible wherever the term appears. It is also framework-neutral across visual, code, research, automation, and application-agent workflows.

## Usage

Use **harness unit** in user-facing text, docs, menus, prompts, and agent instructions.

Use existing command names such as `harneloop init-unit` and `harneloop units` for now to avoid churn. Those commands manage harness units.

Avoid using bare `unit` in user-facing language unless the surrounding phrase already makes the meaning obvious.
