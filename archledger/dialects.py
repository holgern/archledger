from __future__ import annotations

from dataclasses import dataclass

from archledger.model import (
    empty_section_placeholder_for_source_format,
    section_body_placeholder_for_source_format,
)


@dataclass(frozen=True, slots=True)
class Dialect:
    name: str
    record_heading_level: int
    section_placeholder: str
    empty_placeholder: str

    def heading(self, level: int, title: str) -> str:
        raise NotImplementedError

    def discrete_heading(self, level: int, title: str) -> str:
        return self.heading(level, title)

    def table(self, headers: list[str], rows: list[list[str]]) -> str:
        raise NotImplementedError

    def bullet(self, text: str, depth: int = 0) -> str:
        raise NotImplementedError

    def strong(self, text: str) -> str:
        raise NotImplementedError

    def placeholder(self) -> str:
        return self.empty_placeholder


@dataclass(frozen=True, slots=True)
class MarkdownDialect(Dialect):
    def heading(self, level: int, title: str) -> str:
        return f"{'#' * level} {title}"

    def table(self, headers: list[str], rows: list[list[str]]) -> str:
        if not rows:
            return self.placeholder()
        header_row = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        body_rows = ["| " + " | ".join(row) + " |" for row in rows]
        return "\n".join([header_row, separator, *body_rows])

    def bullet(self, text: str, depth: int = 0) -> str:
        return f"{'  ' * depth}- {text}"

    def strong(self, text: str) -> str:
        return f"**{text}**"


@dataclass(frozen=True, slots=True)
class AsciiDocDialect(Dialect):
    def heading(self, level: int, title: str) -> str:
        return f"{'=' * level} {title}"

    def discrete_heading(self, level: int, title: str) -> str:
        return f"[discrete]\n{self.heading(level, title)}"

    def table(self, headers: list[str], rows: list[list[str]]) -> str:
        if not rows:
            return self.placeholder()
        cols = ",".join("1" for _ in headers)
        header_row = "|" + " |".join(headers)
        body_rows = ["|" + " |".join(row) for row in rows]
        return "\n".join(
            [
                f'[cols="{cols}", options="header"]',
                "|===",
                header_row,
                "",
                *body_rows,
                "|===",
            ]
        )

    def bullet(self, text: str, depth: int = 0) -> str:
        return f"{'*' * (depth + 1)} {text}"

    def strong(self, text: str) -> str:
        return f"*{text}*"


def get_dialect(source_format: str) -> Dialect:
    normalized = source_format.strip().lower()
    if normalized == "markdown":
        return MarkdownDialect(
            name="markdown",
            record_heading_level=2,
            section_placeholder=section_body_placeholder_for_source_format(normalized),
            empty_placeholder=empty_section_placeholder_for_source_format(normalized),
        )
    if normalized == "asciidoc":
        return AsciiDocDialect(
            name="asciidoc",
            record_heading_level=3,
            section_placeholder=section_body_placeholder_for_source_format(normalized),
            empty_placeholder=empty_section_placeholder_for_source_format(normalized),
        )
    raise ValueError(f"Unsupported source format: {source_format}")
