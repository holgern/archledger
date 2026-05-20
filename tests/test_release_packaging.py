from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.slow
def test_built_wheel_installed_version_matches_runtime_version(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    _run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist_dir)],
        cwd=PROJECT_ROOT,
    )

    wheels = sorted(dist_dir.glob("archledger-*.whl"))
    assert len(wheels) == 1

    venv_dir = tmp_path / "venv"
    _run([sys.executable, "-m", "venv", str(venv_dir)], cwd=tmp_path)
    venv_python = _venv_executable(venv_dir, "python")

    _run(
        [str(venv_python), "-m", "pip", "install", "--no-deps", str(wheels[0])],
        cwd=tmp_path,
    )

    smoke_dir = tmp_path / "installed-wheel-smoke"
    smoke_dir.mkdir()
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    result = _run(
        [
            str(venv_python),
            "-I",
            "-c",
            (
                "import importlib.metadata; "
                "import archledger; "
                "version = importlib.metadata.version('archledger'); "
                "assert version == archledger.__version__; "
                "print(version)"
            ),
        ],
        cwd=smoke_dir,
        env=env,
    )
    assert result.stdout.strip().startswith("0.")


def _venv_executable(venv_dir: Path, name: str) -> Path:
    scripts_dir = "Scripts" if os.name == "nt" else "bin"
    suffix = ".exe" if os.name == "nt" else ""
    return venv_dir / scripts_dir / f"{name}{suffix}"


def _run(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
