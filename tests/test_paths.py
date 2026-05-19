from __future__ import annotations

from pathlib import Path

from archledger.storage.paths import resolve_project_paths


def test_relative_archledger_dir_is_relative_to_config_path(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "archledger.toml").write_text(
        "\n".join(
            [
                "config_version = 1",
                'archledger_dir = "../shared-state/demo"',
                'project_uuid = "12345678-1234-1234-1234-123456789abc"',
                'project_name = "demo"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    paths, _, warnings = resolve_project_paths(workspace_root)

    assert warnings == []
    assert paths.archledger_dir == (workspace_root / "../shared-state/demo").resolve()


def test_v2_config_supports_new_build_arc42_and_skill_keys(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace-v2"
    workspace_root.mkdir()
    (workspace_root / "archledger.toml").write_text(
        "\n".join(
            [
                "config_version = 2",
                'archledger_dir = ".archledger"',
                'project_uuid = "12345678-1234-1234-1234-123456789abc"',
                'project_name = "demo"',
                "",
                "[build]",
                'default_output = "docs/architecture.md"',
                "include_draft = false",
                "include_superseded = true",
                "strict = false",
                "",
                "[arc42]",
                'template_version = "9.0-EN"',
                'language = "en"',
                'title = "Architecture Documentation"',
                "include_help = true",
                "",
                "[skill]",
                "installed = true",
                'path = "skills/archledger/SKILL.md"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    _, config, warnings = resolve_project_paths(workspace_root)

    assert warnings == []
    assert config.config_version == 2
    assert config.build_include_superseded is True
    assert config.arc42_include_help is True
    assert config.skill_installed is True
    assert config.skill_path == "skills/archledger/SKILL.md"
