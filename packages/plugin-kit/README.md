# Plugin Kit

Shared toolkit for this monorepo.

This package intentionally focuses on scaffolding and templates rather than runtime code.

Why:

- each plugin remains independently publishable
- no shared runtime dependency has to be bundled into standalone plugin exports
- future plugins still get consistent manifests, README structure, and marketplace registration

Templates live under `templates/` and are consumed by `scripts/create-plugin.py`.
