---
schema_version: 2
id: diagram_0002
type: diagram
title: "Building Block Layer Structure"
status: accepted
section: building_block_view
order: 20
date: "2026-05-22"
diagram_type: "unicode"
caption: "Layered decomposition of archledger building blocks"

related_records:
  - white_box_0001
  - black_box_0001
  - black_box_0002
  - black_box_0003
  - black_box_0004
  - black_box_0005
  - black_box_0006
  - black_box_0007
  - black_box_0008
  - black_box_0009
  - black_box_0010
  - black_box_0011
  - black_box_0012
  - black_box_0013
  - black_box_0014
  - black_box_0015

tags:
  - building-block
  - layers
body_format: markdown
created_at: "2026-05-21T19:33:57Z"
updated_at: "2026-05-22T07:15:00Z"
---

The system is organized as a layered pipeline. User input flows down from the
CLI through business logic to storage. Rendering flows upward from storage
through assembly to the build output.

```textdiagram
┌─ Interface ──────────────────────────────────────────────────┐
│  CLI Layer  (cli.py, cli_formatting.py, cli_payloads.py)    │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌─ Business Logic ────────────────────────────────────────────┐
│  Repository (repo.py)        Model (model.py)               │
│  Record Types (rec_types)    Checks (checks.py)             │
│  Source Refs (source_refs.py)                               │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌─ Configuration ────────────────────────────────────────────┐
│  Config Layer (config/)                                    │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌─ Rendering ────────────────────────────────────────────────┐
│  Render (render.py)       Assembly (assembly.py)           │
│  Dialect (dialects.py)    Section Rendering                │
│                           (section_rendering.py)            │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌─ Export ───────────────────────────────────────────────────┐
│  Converter (converters, conversion_plan, formats)          │
│  Migration (migration.py)                                  │
└────────────────────────────┬─────────────────────────────────┘
                             ▼
┌─ Infrastructure ───────────────────────────────────────────┐
│  Storage (storage/)         Source Tracking                 │
│                             (source_tracking.py)            │
└────────────────────────────────────────────────────────────┘
```
