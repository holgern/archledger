from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_ID_PREFIX = "al"
DEFAULT_ID_WIDTH = 4
ID_PREFIX_PATTERN = re.compile(r"^[a-z][a-z0-9]{1,15}$")
_WORD_CHAR_CLASS = "A-Za-z0-9"


@dataclass(frozen=True, slots=True)
class LedgerIdFormat:
    prefix: str = DEFAULT_ID_PREFIX
    width: int = DEFAULT_ID_WIDTH

    def __post_init__(self) -> None:
        validate_id_prefix(self.prefix)
        validate_id_width(self.width)

    @property
    def pattern_text(self) -> str:
        escaped = re.escape(self.prefix)
        return rf"^{escaped}_(?P<number>\d{{{self.width},}})$"

    @property
    def reference_pattern_text(self) -> str:
        escaped = re.escape(self.prefix)
        return (
            rf"(?<![{_WORD_CHAR_CLASS}])"
            rf"{escaped}_(?P<number>\d{{{self.width},}})"
            rf"(?![{_WORD_CHAR_CLASS}])"
        )

    def pattern(self) -> re.Pattern[str]:
        return re.compile(self.pattern_text)

    def reference_pattern(self) -> re.Pattern[str]:
        return re.compile(self.reference_pattern_text)

    def format(self, number: int) -> str:
        return format_ledger_id(number, prefix=self.prefix, width=self.width)

    def parse(self, record_id: str) -> int:
        return parse_ledger_id(record_id, prefix=self.prefix, width=self.width)

    def is_id(self, value: object) -> bool:
        return is_ledger_id(value, prefix=self.prefix, width=self.width)


def validate_id_prefix(prefix: str) -> str:
    normalized = prefix.strip()
    if not ID_PREFIX_PATTERN.fullmatch(normalized):
        raise ValueError("Ledger ID prefix must match ^[a-z][a-z0-9]{1,15}$.")
    return normalized


def validate_id_width(width: int) -> int:
    if isinstance(width, bool) or not isinstance(width, int) or not 2 <= width <= 12:
        raise ValueError("Ledger ID width must be an integer from 2 to 12.")
    return width


def format_ledger_id(
    number: int,
    *,
    prefix: str = DEFAULT_ID_PREFIX,
    width: int = DEFAULT_ID_WIDTH,
) -> str:
    if isinstance(number, bool) or not isinstance(number, int) or number < 1:
        raise ValueError("Ledger ID number must be a positive integer.")
    normalized_prefix = validate_id_prefix(prefix)
    validated_width = validate_id_width(width)
    return f"{normalized_prefix}_{number:0{validated_width}d}"


def parse_ledger_id(
    record_id: str,
    *,
    prefix: str = DEFAULT_ID_PREFIX,
    width: int = DEFAULT_ID_WIDTH,
) -> int:
    normalized_prefix = validate_id_prefix(prefix)
    validated_width = validate_id_width(width)
    match = re.fullmatch(
        rf"{re.escape(normalized_prefix)}_(?P<number>\d{{{validated_width},}})",
        record_id,
    )
    if match is None:
        raise ValueError(f"Invalid ledger ID: {record_id!r}")
    number = int(match.group("number"))
    if number < 1:
        raise ValueError(f"Invalid ledger ID: {record_id!r}")
    return number


def is_ledger_id(
    value: object,
    *,
    prefix: str = DEFAULT_ID_PREFIX,
    width: int = DEFAULT_ID_WIDTH,
) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parse_ledger_id(value, prefix=prefix, width=width)
    except ValueError:
        return False
    return True


def filename_for_ledger_id(
    record_id: str,
    extension: str = ".md",
    *,
    prefix: str = DEFAULT_ID_PREFIX,
    width: int = DEFAULT_ID_WIDTH,
) -> str:
    parse_ledger_id(record_id, prefix=prefix, width=width)
    return f"{record_id}{extension}"


def ledger_id_from_filename(
    path: Path,
    *,
    prefix: str = DEFAULT_ID_PREFIX,
    width: int = DEFAULT_ID_WIDTH,
) -> str:
    record_id = path.stem
    parse_ledger_id(record_id, prefix=prefix, width=width)
    return record_id
