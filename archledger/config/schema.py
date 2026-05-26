"""Declarative config schema for data-driven TOML parsing and rendering.

This module defines lightweight spec types that describe config tables and
their fields.  Both the parser (``config/parse.py``) and the renderer
(``config/render.py``) can share these specs so that field names, defaults,
allowed values, and validation logic stay in one place.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class FieldSpec:
    """Describes one field inside a config table.

    Parameters
    ----------
    name:
        TOML key name.
    default:
        Default value used when the key is absent.
    parse:
        Callable ``(raw_value, field_name) -> parsed_value``.
        Should raise :class:`~archledger.errors.ConfigError` on invalid input.
    render:
        Optional callable ``(parsed_value) -> raw_value`` for rendering back
        to TOML.  Defaults to the identity function.
    """

    name: str
    default: Any = None
    parse: Callable[[object, str], Any] | None = None
    render: Callable[[Any], Any] | None = None


@dataclass(frozen=True, slots=True)
class TableSpec:
    """Describes one TOML table (``[table_name]``).

    Parameters
    ----------
    name:
        TOML table name (e.g. ``"ids"``, ``"tracking"``).
    fields:
        Ordered tuple of field specs.
    factory:
        Callable that receives parsed field values as keyword arguments and
        returns the config dataclass instance.
    """

    name: str
    fields: tuple[FieldSpec, ...]
    factory: Callable[..., Any]


def parse_table_from_spec(
    table_data: dict[str, object],
    spec: TableSpec,
) -> dict[str, Any]:
    """Parse a TOML table dict according to a :class:`TableSpec`.

    Returns a dict of ``{field_name: parsed_value}`` suitable for
    passing to the spec's factory as ``**kwargs``.
    """
    result: dict[str, Any] = {}
    for field in spec.fields:
        raw = table_data.get(field.name, field.default)
        if field.parse is not None:
            result[field.name] = field.parse(raw, f"{spec.name}.{field.name}")
        else:
            result[field.name] = raw
    return result
