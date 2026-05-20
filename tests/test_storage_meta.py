from __future__ import annotations

from pathlib import Path

import pytest

from archledger.errors import StorageError
from archledger.storage.meta import read_storage_meta


def test_storage_counter_bool_is_rejected(tmp_path: Path) -> None:
    storage = tmp_path / "storage.yaml"
    storage.write_text(
        "\n".join(
            [
                "storage_version: 1",
                'created_with_archledger: "0.1.dev10"',
                'project_uuid: "00000000-0000-4000-8000-000000000000"',
                'created_at: "2026-05-20T00:00:00Z"',
                "next_numbers:",
                "  requirement: true",
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(StorageError, match="next_numbers"):
        read_storage_meta(storage)
