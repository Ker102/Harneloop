# Product Principles

EvoRig is the temporary working name for the prototype. The final name can change without changing the architecture.

## What This Is

EvoRig is a framework agents use to build and improve the harness around themselves or another target agent.

The framework should help agents:

- run task attempts;
- inspect real artifacts;
- trace failures back to runs;
- maintain a unit-local operational map of workflow, evidence, environment assumptions, and open questions;
- propose candidate harness patches;
- test candidate patches;
- promote only evidence-backed improvements;
- package portable harness units.

## What This Is Not

EvoRig is not:

- a generic eval dashboard;
- a fixed agent graph framework;
- a Blender-specific system;
- a model-training or fine-tuning system;
- a loose folder of prompts with no lifecycle.

## Core Design Tension

The system is built for generative AI models, so it must leave room for reasoning and exploration. At the same time, the framework must protect lifecycle integrity.

The rule:

> Agents can explore freely inside candidates. The engine controls promotion.

`operational-map.md` exists to preserve the agent's current working understanding of a harness unit without turning that understanding into a fixed script. The agent should use it to orient itself, update it as evidence changes, and still reason from the current task and artifacts.
