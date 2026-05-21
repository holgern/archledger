---
id: section_solution_strategy
type: section
section: solution_strategy
title: Solution Strategy
schema_version: 2
date: "2026-05-21"
body_format: markdown
order: 40
status: accepted
---

The fundamental approach is a file-based pipeline: human-editable Markdown or AsciiDoc records with YAML front matter are stored in a configurable directory, validated by a check command, assembled into a single arc42-style document by a Jinja2-based render step, and optionally converted to other formats (HTML, PDF, DOCX, RST, Textile) via pandoc or asciidoctor. A dialect abstraction (`dialects.py`) ensures that rendering logic works identically for both source formats. The CLI provides the sole interface. No server, database, or GUI is involved.

A source tracking subsystem (`source snapshot`/`source changed`) allows agents to detect which source files changed since the last baseline and which architecture records are impacted via `source_refs` linkage.

Build pipeline (portable text diagram):

```text
config discovery
      |
      v
load sections + records
      |
      v
validate/check rules
      |
      v
assemble native arc42 document
      |
      +--> optional converter execution (pandoc/asciidoctor)
      |
      v
write output artifact(s)
```
