# Compact Lifecycle Visual

## Goal

Provide a small Harneloop lifecycle diagram that stays readable in GitHub Markdown and can be formatted into a roughly 4:3 image without tangled connector lines.

## Layout

The graph uses three stacked horizontal stages:

1. Observe: goal, attempt, and evidence inspection.
2. Improve: diagnosis, candidate creation, and retesting.
3. Decide: evidence gate, promotion, or revision.

The rejected path ends in a local `Revise candidate and repeat` node instead of drawing a long edge back across earlier stages. The surrounding text explains that this returns to diagnosis. This keeps the conceptual loop while preventing Mermaid from reordering the stages or crossing connectors.

## Validation

Render the raw Mermaid source at 1200 by 900 pixels and inspect the result for stage order, text wrapping, aspect ratio, and connector crossings. Keep the detailed architecture graph unchanged for readers who need capability, human-review, wait, and stop branches.
