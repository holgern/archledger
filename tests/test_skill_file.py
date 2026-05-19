from __future__ import annotations

from pathlib import Path


def test_archledger_skill_exists() -> None:
    skill = Path("skills/archledger/SKILL.md")
    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "archledger --json where" in text
    assert "archledger --json check" in text
    assert "archledger build" in text
    assert "archledger seed arc42-minimal" in text
    assert "generated build output" in text.lower()
