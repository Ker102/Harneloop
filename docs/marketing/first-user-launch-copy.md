# First-user Launch Copy

Replace `[Project name]` and `[repository link]` after the final rename. Keep benchmark claims scoped to the published ViperMesh case study.

## Core One-liner

`[Project name]` is an open-source framework that lets agents build and evolve portable, task-specific harnesses through real attempts, artifact inspection, traced failures, and evidence-gated candidate promotion.

## Discord

I am building `[Project name]`, an open-source self-evolving harness framework for AI agents. You give an agent a specific task to improve, and it creates a portable harness unit around that task. It runs real attempts, inspects artifacts and traces, diagnoses likely failures, proposes changes to its tools, context, instructions, or validators, and retests them. The working harness is not replaced until evidence shows that the candidate improves performance without unacceptable regressions.

The first case study used this process to develop a Blender spatial-reasoning harness. With the same acting model in both lanes, the evolved harness was faster on 6 of 7 comparable live tasks and used substantially fewer local acting-agent tokens on the documented comparable pair. I am looking for a small number of design partners with a recurring agent task to test next: `[repository link]`.

## X / Twitter

Building `[Project name]`: an open-source framework where agents evolve portable harness units for specific tasks. They run real attempts, inspect artifacts and traces, diagnose failures, test candidate changes, and promote only proven improvements. Same model, better harness. Looking for early users: `[repository link]`

Suggested follow-up post:

The first case study used the framework to develop a Blender spatial-reasoning harness. Against the Anthropic x Blender MCP baseline, with the same acting model, it was faster on 6/7 comparable live tasks with a 2.534x mean speedup. Methodology and limitations: https://www.kristoferjussmann.me/case-studies/vipermesh

## Reddit

### Title

I built a framework that lets agents improve their own task-specific harnesses through evidence-backed trial and error

### Body

`[Project name]` is an open-source, agent-first framework for building portable harness units around specific tasks. The operating agent runs the real task, captures artifacts, logs, traces, and structured state, compares the result with the target, and traces likely mistakes through the recorded run. It develops changes inside an isolated candidate workspace and reruns relevant and regression tasks. The active harness is promoted only when the evidence supports an improvement.

This is not another agent runtime or an evaluation dashboard. It is a structured way for agents to improve prompts, context, tools, retrieval, validators, and environment automation without letting self-modification drift outside a verifiable lifecycle. Agents remain free to reason and add what the task needs; the framework protects evidence, versioning, rollback, and promotion.

The first case study used it to develop a Blender spatial-reasoning harness. With the same acting model in both comparison lanes, the evolved harness was faster on 6 of 7 comparable live tasks, achieved a 2.534x mean speedup, and significantly reduced local acting-agent token usage on the documented comparable pair. I am looking for early users with a recurring agent failure and a real environment where we can build the next harness unit.

- Repository: `[repository link]`
- Case study: https://www.kristoferjussmann.me/case-studies/vipermesh

## Claims Boundary

Do not claim that the framework outperforms every form of fine-tuning. The current evidence supports a harness-first position: task-specific harness improvements can produce large, inspectable, reversible gains without changing model weights, and fine-tuning remains useful in other settings or alongside a strong harness.
