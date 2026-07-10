# Security

Harneloop is a local-first framework for agent-built harness units. Security boundaries matter because agents may create tools, run commands, and package reusable units.

## Current Status

This is a private pre-alpha prototype. Do not treat it as a hardened sandbox.

## Rules

- Never store secrets inside harness units.
- Do not package `.env` files, private keys, credentials, caches, or raw runtime traces by default.
- Treat generated candidate tools as untrusted until inspected.
- Use framework commands for promotion, rollback, and packaging.
- Keep destructive actions behind explicit user approval.

## Reporting

For now, report issues directly to the repository owner. A public security policy can be added before open-source release.
