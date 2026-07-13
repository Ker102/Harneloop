# Security

Harneloop is a local-first framework for agent-built harness units. Security boundaries matter because agents may create tools, run commands, and package reusable units.

## Current Status

This is an early public alpha. Do not treat Harneloop or a harness unit as a hardened sandbox or security boundary.

## Rules

- Never store secrets inside harness units.
- Do not package `.env` files, private keys, credentials, caches, or raw runtime traces by default.
- Treat generated candidate tools as untrusted until inspected.
- Use framework commands for promotion, rollback, and packaging.
- Keep destructive actions behind explicit user approval.

## Reporting

Do not disclose suspected vulnerabilities in a public issue. Use GitHub's private vulnerability reporting form when it is available for this repository. Otherwise, contact the repository owner privately through the linked GitHub profile and include reproduction details, affected versions, and potential impact.
