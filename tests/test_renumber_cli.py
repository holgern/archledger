from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from archledger.cli import app

runner = CliRunner()


def init_project(tmp_path: Path, *, source_format: str = "asciidoc") -> None:
    result = runner.invoke(
        app,
        ["--root", str(tmp_path), "init", "--source-format", source_format],
    )
    assert result.exit_code == 0, result.stdout


def test_renumber_dry_run_does_not_mutate(tmp_path: Path) -> None:
    init_project(tmp_path)
    create = runner.invoke(
        app,
        ["--root", str(tmp_path), "new", "requirement", "A"],
    )
    assert create.exit_code == 0
    old_path = tmp_path / ".archledger" / "records" / "requirements" / "al_0013.adoc"

    result = runner.invoke(
        app,
        [
            "--root",
            str(tmp_path),
            "--json",
            "renumber",
            "--prefix",
            "ta",
            "--width",
            "3",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["result"]["apply"] is False
    assert payload["result"]["renamed_count"] == 13
    assert old_path.is_file()
    assert not (
        tmp_path / ".archledger" / "records" / "requirements" / "ta_013.adoc"
    ).exists()


def test_renumber_apply_renames_files_updates_frontmatter_and_config(
    tmp_path: Path,
) -> None:
    init_project(tmp_path)
    parent_result = runner.invoke(
        app,
        ["--root", str(tmp_path), "new", "white-box", "Parent"],
    )
    assert parent_result.exit_code == 0
    child_result = runner.invoke(
        app,
        [
            "--root",
            str(tmp_path),
            "new",
            "white-box",
            "Child",
            "--parent",
            "al_0013",
        ],
    )
    assert child_result.exit_code == 0

    result = runner.invoke(
        app,
        [
            "--root",
            str(tmp_path),
            "--json",
            "renumber",
            "--prefix",
            "ta",
            "--width",
            "3",
            "--apply",
        ],
    )

    assert result.exit_code == 0
    assert not (
        tmp_path / ".archledger" / "records" / "building_blocks" / "al_0013.adoc"
    ).exists()
    child = tmp_path / ".archledger" / "records" / "building_blocks" / "ta_014.adoc"
    assert child.is_file()
    child_text = child.read_text(encoding="utf-8")
    assert "id: ta_014" in child_text
    assert "parent: ta_013" in child_text
    assert "al_0013" not in child_text

    config_text = (tmp_path / "archledger.toml").read_text(encoding="utf-8")
    assert "[ids]" in config_text
    assert 'prefix = "ta"' in config_text
    assert "width = 3" in config_text

    check = runner.invoke(app, ["--root", str(tmp_path), "check"])
    assert check.exit_code == 0


def test_renumber_apply_includes_archive_tombstones(tmp_path: Path) -> None:
    init_project(tmp_path)
    create = runner.invoke(
        app,
        ["--root", str(tmp_path), "new", "requirement", "A"],
    )
    assert create.exit_code == 0
    missing = tmp_path / ".archledger" / "records" / "requirements" / "al_0013.adoc"
    missing.unlink()
    repair = runner.invoke(app, ["--root", str(tmp_path), "doctor", "--repair"])
    assert repair.exit_code == 0, repair.output

    result = runner.invoke(
        app,
        [
            "--root",
            str(tmp_path),
            "renumber",
            "--prefix",
            "ta",
            "--width",
            "3",
            "--apply",
        ],
    )

    assert result.exit_code == 0
    assert (
        tmp_path / ".archledger" / "archive" / "tombstones" / "ta_013.adoc"
    ).is_file()
    assert not (
        tmp_path / ".archledger" / "archive" / "tombstones" / "al_0013.adoc"
    ).exists()


def test_renumber_rejects_invalid_prefix(tmp_path: Path) -> None:
    init_project(tmp_path)
    result = runner.invoke(
        app,
        ["--root", str(tmp_path), "renumber", "--prefix", "TA", "--width", "3"],
    )
    assert result.exit_code == 1
    assert "prefix" in result.stderr.lower() or "prefix" in result.stdout.lower()


def test_renumber_rejects_existing_target_file(tmp_path: Path) -> None:
    init_project(tmp_path)
    target = tmp_path / ".archledger" / "sections" / "ta_001.adoc"
    target.write_text("do not overwrite\n", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "--root",
            str(tmp_path),
            "renumber",
            "--prefix",
            "ta",
            "--width",
            "3",
            "--apply",
        ],
    )

    assert result.exit_code == 1
    assert target.read_text(encoding="utf-8") == "do not overwrite\n"
