# Codex Plugins

Local monorepo for Codex plugins.

## Why this layout

This repo is the development home for multiple plugins.

Each plugin stays self-contained under `plugins/<plugin-name>` so it can still be exported and published as a standalone repo when needed.

This monorepo is the source of truth.

Standalone plugin repos are derived outputs. Do not edit a published standalone repo directly and expect those changes to remain authoritative.

Shared logic lives at the repo level as toolkit templates and scaffolding scripts rather than hard runtime dependencies. That keeps publishing cleaner: future plugins can reuse the same generator and templates without forcing cross-plugin package coupling.

## Layout

```text
.agents/plugins/marketplace.json
packages/plugin-kit/
plugins/upwork-autopilot/
scripts/create-plugin.py
scripts/export-plugin.sh
scripts/sync-standalone-repo.sh
```

## Current plugins

- `upwork-autopilot`

## Create a new plugin

```bash
cd codex-plugins
python3 scripts/create-plugin.py my-plugin
```

That will:

- normalize the plugin name
- create `plugins/<plugin-name>/`
- scaffold `.codex-plugin/plugin.json`, `README.md`, `package.json`, and a starter `SKILL.md`
- create `skills/`, `scripts/`, and `assets/`
- register the plugin in `.agents/plugins/marketplace.json`

## Use in Codex

Open this repo in Codex and it will use the repo-local marketplace at `.agents/plugins/marketplace.json`.

## Validation

Run:

```bash
bash scripts/validate-workspace.sh
```

## Sync to a standalone repo

Export a plugin:

```bash
bash scripts/export-plugin.sh upwork-autopilot
```

Sync that exported plugin into a standalone git checkout:

```bash
bash scripts/sync-standalone-repo.sh upwork-autopilot /absolute/path/to/standalone-repo
```

The detailed workflow is in [docs/WORKFLOW.md](./docs/WORKFLOW.md).

## Publishing model

- develop plugins here
- keep shared scaffolding in `packages/plugin-kit`
- export individual plugins as standalone repos when they are ready to publish

For `upwork-autopilot`, the standalone GitHub repo remains separate and already published.
