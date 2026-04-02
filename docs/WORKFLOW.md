# Plugin Workflow

## Source of truth

`plugins/<plugin-name>` inside this monorepo is the canonical source.

Published standalone repositories are distribution targets, not authoring targets.

## Day-to-day development

1. Edit the plugin under `plugins/<plugin-name>`
2. Run `bash scripts/validate-workspace.sh`
3. Export the plugin with `bash scripts/export-plugin.sh <plugin-name>`
4. If the plugin has a standalone git checkout, sync it with `bash scripts/sync-standalone-repo.sh <plugin-name> /abs/path/to/repo`
5. Commit and push from the standalone repo only after the sync step

## Why this rule exists

Without a clear promotion flow, the monorepo plugin and the standalone published repo will drift.

This repo avoids that by making the monorepo authoritative and the standalone repo reproducible.

## Upwork Autopilot

`plugins/upwork-autopilot` is the development source.

Its published standalone repository is:

- [klajdikkolaj/upwork-autopilot](https://github.com/klajdikkolaj/upwork-autopilot)
