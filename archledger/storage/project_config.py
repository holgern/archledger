from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast
from uuid import UUID, uuid4

from archledger.errors import ConfigError
from archledger.storage.common import read_text

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib


_ALLOWED_TOP_LEVEL_KEYS = {
    "config_version",
    "archledger_dir",
    "project_uuid",
    "project_name",
    "build",
    "arc42",
    "skill",
}
_ALLOWED_BUILD_KEYS = {
    "default_output",
    "include_draft",
    "include_superseded",
    "strict",
}
_ALLOWED_ARC42_KEYS = {"template_version", "language", "title", "include_help"}
_ALLOWED_SKILL_KEYS = {"installed", "path"}


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    config_version: int
    archledger_dir: str
    project_uuid: str
    project_name: str
    build_default_output: str = "architecture.md"
    build_include_draft: bool = False
    build_include_superseded: bool = False
    build_strict: bool = False
    arc42_template_version: str = "9.0-EN"
    arc42_language: str = "en"
    arc42_title: str = "Architecture Documentation"
    arc42_include_help: bool = False
    skill_installed: bool = False
    skill_path: str = "skills/archledger/SKILL.md"


def normalize_project_name(name: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", name.strip().lower()).strip("-")
    if not normalized:
        raise ConfigError("Project name must contain at least one letter or number.")
    return normalized


def render_default_config(
    workspace_root: Path,
    *,
    archledger_dir: str,
    project_name: str | None = None,
    project_uuid: str | None = None,
) -> str:
    normalized_project_name = normalize_project_name(
        workspace_root.name if project_name is None else project_name
    )
    normalized_uuid = (
        str(uuid4()) if project_uuid is None else _validate_uuid(project_uuid)
    )
    return "\n".join(
        [
            "# Project-local archledger configuration.",
            "# This file lives in the source project root.",
            "config_version = 2",
            f'archledger_dir = "{archledger_dir}"',
            "",
            "# Stable project identity. Commit this with your source tree.",
            f'project_uuid = "{normalized_uuid}"',
            f'project_name = "{normalized_project_name}"',
            "",
            "[build]",
            'default_output = "architecture.md"',
            "include_draft = false",
            "include_superseded = false",
            "strict = false",
            "",
            "[arc42]",
            'template_version = "9.0-EN"',
            'language = "en"',
            'title = "Architecture Documentation"',
            "include_help = false",
            "",
            "[skill]",
            "installed = true",
            'path = "skills/archledger/SKILL.md"',
            "",
        ]
    )


def load_project_config(path: Path) -> ProjectConfig:
    try:
        raw_data = tomllib.loads(read_text(path))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Failed to parse {path.name}: {exc}") from exc

    if not isinstance(raw_data, dict):
        raise ConfigError(f"{path.name} did not parse to a TOML table.")

    unknown_top_level = sorted(set(raw_data) - _ALLOWED_TOP_LEVEL_KEYS)
    if unknown_top_level:
        joined = ", ".join(unknown_top_level)
        raise ConfigError(f"Unknown config keys in {path.name}: {joined}")

    build_data = _validate_subtable(
        path,
        raw_data.get("build"),
        _ALLOWED_BUILD_KEYS,
        "build",
    )
    arc42_data = _validate_subtable(
        path,
        raw_data.get("arc42"),
        _ALLOWED_ARC42_KEYS,
        "arc42",
    )
    skill_data = _validate_subtable(
        path,
        raw_data.get("skill"),
        _ALLOWED_SKILL_KEYS,
        "skill",
    )

    config_version = raw_data.get("config_version")
    if config_version not in {1, 2}:
        raise ConfigError("config_version must be 1 or 2.")

    archledger_dir = raw_data.get("archledger_dir")
    if not isinstance(archledger_dir, str) or not archledger_dir.strip():
        raise ConfigError("archledger_dir must be a non-empty string.")

    project_uuid = raw_data.get("project_uuid")
    if not isinstance(project_uuid, str):
        raise ConfigError("project_uuid must be a string.")

    project_name = raw_data.get("project_name")
    if not isinstance(project_name, str):
        raise ConfigError("project_name must be a string.")

    default_output = build_data.get("default_output", "architecture.md")
    if not isinstance(default_output, str) or not default_output.strip():
        raise ConfigError("build.default_output must be a non-empty string.")

    include_draft = build_data.get("include_draft", False)
    include_superseded = build_data.get("include_superseded", False)
    strict = build_data.get("strict", False)
    if not all(
        isinstance(value, bool)
        for value in (include_draft, include_superseded, strict)
    ):
        raise ConfigError(
            "build.include_draft, build.include_superseded, and build.strict "
            "must be booleans."
        )

    template_version = arc42_data.get("template_version", "9.0-EN")
    language = arc42_data.get("language", "en")
    title = arc42_data.get("title", "Architecture Documentation")
    include_help = arc42_data.get("include_help", False)
    if not all(
        isinstance(value, str) and value.strip()
        for value in (template_version, language, title)
    ):
        raise ConfigError(
            "arc42.template_version, arc42.language, and arc42.title "
            "must be non-empty strings."
        )
    if not isinstance(include_help, bool):
        raise ConfigError("arc42.include_help must be a boolean.")

    skill_installed = skill_data.get("installed", False)
    skill_path = skill_data.get("path", "skills/archledger/SKILL.md")
    if not isinstance(skill_installed, bool):
        raise ConfigError("skill.installed must be a boolean.")
    if not isinstance(skill_path, str) or not skill_path.strip():
        raise ConfigError("skill.path must be a non-empty string.")

    return ProjectConfig(
        config_version=cast(int, config_version),
        archledger_dir=archledger_dir,
        project_uuid=_validate_uuid(project_uuid),
        project_name=normalize_project_name(project_name),
        build_default_output=default_output,
        build_include_draft=include_draft,
        build_include_superseded=include_superseded,
        build_strict=strict,
        arc42_template_version=cast(str, template_version),
        arc42_language=cast(str, language),
        arc42_title=cast(str, title),
        arc42_include_help=include_help,
        skill_installed=skill_installed,
        skill_path=skill_path,
    )


def _validate_subtable(
    path: Path,
    value: object,
    allowed_keys: set[str],
    table_name: str,
) -> dict[str, object]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError(f"{table_name} in {path.name} must be a TOML table.")
    unknown_keys = sorted(set(value) - allowed_keys)
    if unknown_keys:
        joined = ", ".join(unknown_keys)
        raise ConfigError(f"Unknown keys in {table_name}: {joined}")
    return dict(value)


def _validate_uuid(value: str) -> str:
    try:
        return str(UUID(value))
    except ValueError as exc:
        raise ConfigError("project_uuid must be a valid UUID.") from exc
