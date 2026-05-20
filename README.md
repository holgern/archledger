# archledger

`archledger` is an arc42-oriented architecture documentation ledger that stores canonical source fragments as YAML front matter plus either Markdown or AsciiDoc bodies. It keeps a small project-local `archledger.toml` in the workspace and stores human-editable section and record sources under a configurable `archledger_dir`.

## What archledger is

`archledger` is intentionally small:

- project-local config discovery from `archledger.toml` or `.archledger.toml`
- dual-source canonical fragments in Markdown or AsciiDoc
- a compact Typer CLI for init, read, record creation, validation, migration, and builds
- deterministic native document assembly with optional export formats

It is **not** a task tracker, workflow engine, lock manager, or sync tool.

## Install

```bash
python -m pip install -e .
archledger --version
```

## Quick start

Markdown project:

```bash
archledger init --source-format markdown
archledger seed arc42-minimal
archledger --json read --include-body
archledger build --format markdown
```

AsciiDoc project:

```bash
archledger init --source-format asciidoc
archledger seed arc42-minimal
archledger --json read --include-body
archledger build --format asciidoc
```

Useful supporting commands:

```bash
archledger status
archledger where
archledger list --include-draft
archledger show black_box_0001
archledger read --include-body --include-draft
archledger convert-sources --to asciidoc --write
```

## Canonical source model

Markdown and AsciiDoc are both first-class source formats. The individual section and record fragments under `archledger_dir` are the source of truth. Generated complete documents under `.archledger/build/` are derived artifacts and must not be edited as canonical source.

Example front matter:

```yaml
---
schema_version: 2
id: adr0001
type: adr
title: "Treat source fragments as canonical"
status: accepted
section: architecture_decisions
order: 10
date: "2026-05-20"
body_format: markdown
created_at: "2026-05-20T00:00:00Z"
updated_at: "2026-05-20T00:00:00Z"
---
```

## Reading docs without exporting

Use `read` to inspect the current source state directly:

```bash
archledger --json where
archledger --json status
archledger --json check
archledger --json read --include-body --include-draft
archledger --json read --section building_block_view --include-body
archledger --json read --kind adr --include-body
```

`read` does not call the build pipeline and does not create `.archledger/build` outputs.

## Build matrix

| Source format | Output format | Tooling |
| --- | --- | --- |
| Markdown | Markdown | none |
| AsciiDoc | AsciiDoc | none |
| Markdown | HTML, DOCX, RST, Textile, PDF, AsciiDoc | `pandoc` |
| AsciiDoc | HTML | `asciidoctor` |
| AsciiDoc | PDF | `asciidoctor-pdf` |
| AsciiDoc | DOCX, Markdown, RST, Textile | `asciidoctor` + `pandoc` |

Examples:

```bash
archledger build --format markdown
archledger build --format asciidoc
archledger build --format html
archledger build --formats html,markdown
archledger --json build --formats html,markdown
```

Optional tool notes:

- Markdown-source exports use `pandoc`.
- AsciiDoc HTML uses `asciidoctor`.
- AsciiDoc PDF uses `asciidoctor-pdf`.
- AsciiDoc DOCX/Markdown/RST/Textile exports use Asciidoctor DocBook plus `pandoc`.

## Storage layout

By default, `archledger init` writes `archledger.toml` at the workspace root and stores state under `.archledger/`.

```text
archledger.toml
.archledger/
  storage.yaml
  sections/
    01_introduction_and_goals.md|adoc
    ...
    12_glossary.md|adoc
  records/
    requirements/
    building_blocks/
    concepts/
    constraints/
    contexts/
    decisions/
    deployment/
    glossary/
    quality_goals/
    quality_requirements/
    quality_scenarios/
    risks/
    runtime/
    stakeholders/
    strategy/
  build/
    architecture.md
    architecture.adoc
    architecture.html
    architecture.pdf
    architecture.docx
    architecture.rst
    architecture.textile
```

Relative `archledger_dir` values are resolved from the config file directory. Absolute paths are used as-is.

## Agent guidance

- Prefer `--json` for automation.
- Read source fragments directly with `archledger --json read --include-body` before building artifacts.
- Use `archledger check` before `archledger build` when mutating records programmatically.
- Treat `.archledger/build/*` as generated output, not source.
- Use `convert-sources` only when the user explicitly wants a dialect migration.

## Skill

The repository-provided agent protocol lives at `skills/archledger/SKILL.md`.
