#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def normalize_plugin_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not normalized:
        raise ValueError("Plugin name must contain at least one alphanumeric character.")
    if len(normalized) > 64:
        raise ValueError("Plugin name must be 64 characters or fewer after normalization.")
    return normalized


def to_display_name(plugin_name: str) -> str:
    return " ".join(part.capitalize() for part in plugin_name.split("-"))


def render_template(path: Path, replacements: dict[str, str]) -> str:
    content = path.read_text()
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def update_marketplace(path: Path, plugin_name: str) -> None:
    entry = {
        "name": plugin_name,
        "source": {
            "source": "local",
            "path": f"./plugins/{plugin_name}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }

    if path.exists():
        payload = json.loads(path.read_text())
    else:
        payload = {
            "name": "local-plugins",
            "interface": {"displayName": "Local Plugins"},
            "plugins": [],
        }

    plugins = payload.setdefault("plugins", [])
    if not any(plugin.get("name") == plugin_name for plugin in plugins if isinstance(plugin, dict)):
        plugins.append(entry)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new plugin in this monorepo.")
    parser.add_argument("name", help="Plugin name. Will be normalized to lower-case hyphen-case.")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffolded files if they exist.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repo root override for testing.",
    )
    args = parser.parse_args()

    repo_root = args.root.resolve()
    plugin_name = normalize_plugin_name(args.name)
    display_name = to_display_name(plugin_name)
    plugin_root = repo_root / "plugins" / plugin_name
    template_root = repo_root / "packages" / "plugin-kit" / "templates"
    marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"

    required_templates = [
        template_root / "README.md.tmpl",
        template_root / "package.json.tmpl",
        template_root / "plugin.json.tmpl",
    ]
    missing_templates = [str(path) for path in required_templates if not path.exists()]
    if missing_templates:
        raise FileNotFoundError(
            "Missing plugin-kit template files:\n- " + "\n- ".join(missing_templates)
        )

    replacements = {
        "PLUGIN_NAME": plugin_name,
        "DISPLAY_NAME": display_name,
    }

    skills_root = plugin_root / "skills" / plugin_name
    skills_root.mkdir(parents=True, exist_ok=True)
    (plugin_root / "scripts").mkdir(parents=True, exist_ok=True)
    (plugin_root / "assets").mkdir(parents=True, exist_ok=True)

    write_file(
        plugin_root / "README.md",
        render_template(template_root / "README.md.tmpl", replacements),
        args.force,
    )
    write_file(
        plugin_root / "package.json",
        render_template(template_root / "package.json.tmpl", replacements),
        args.force,
    )
    write_file(
        plugin_root / ".codex-plugin" / "plugin.json",
        render_template(template_root / "plugin.json.tmpl", replacements),
        args.force,
    )
    write_file(
        skills_root / "SKILL.md",
        render_template(template_root / "SKILL.md.tmpl", replacements),
        args.force,
    )

    update_marketplace(marketplace_path, plugin_name)

    print(f"Created plugin scaffold at {plugin_root}")
    print(f"Registered {plugin_name} in {marketplace_path}")


if __name__ == "__main__":
    main()
