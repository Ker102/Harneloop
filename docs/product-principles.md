# Product Principles

EvoRig is the temporary working name for the prototype. The final name can change without changing the architecture.

## What This Is

EvoRig is a framework agents use to build and improve the harness around themselves or another target agent.

The framework should help agents:

- run task attempts;
- inspect real artifacts;
- trace failures back to runs;
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
