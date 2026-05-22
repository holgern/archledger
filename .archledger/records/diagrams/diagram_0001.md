---
schema_version: 2
id: diagram_0001
type: diagram
title: "System Context"
status: accepted
section: context_and_scope
order: 10
date: "2026-05-21"
diagram_type: "unicode"
caption: "archledger system context showing external actors and adjacent systems"

related_records:
  - context_interface_0001
  - context_interface_0002
  - context_interface_0003
  - context_interface_0004

tags:
  - context
body_format: markdown
created_at: "2026-05-21T19:33:47Z"
updated_at: "2026-05-22T07:15:00Z"
---

archledger operates as a local CLI tool. External actors interact through shell invocations. Optional converter tools (pandoc, asciidoctor) are invoked as subprocesses for non-native export formats.

```textdiagram
┌───────────┐  ┌──────────────┐  ┌──────────────┐
│ Developer │  │ Coding Agent │  │ CI Pipeline  │
└─────┬─────┘  └──────┬───────┘  └──────┬───────┘
      │               │                 │
      └───────────────┼─────────────────┘
                      ▼
           ┌─────────────────────┐
           │   archledger CLI    │
           │  (Typer entrypoint) │
           └─────┬─────────┬─────┘
                 │         │
      ┌──────────▼───┐ ┌───▼──────────────┐
      │  Workspace   │ │  Build Output    │
      │ .archledger/ │ │ ARCHITECTURE.md  │
      │  records/    │ │  + exports       │
      └──────────────┘ └───┬──────────┬────┘
                             │          │
                      ┌──────▼───┐ ┌───▼───────────┐
                      │  pandoc  │ │ asciidoctor   │
                      │ optional │ │   optional    │
                      └──────────┘ └──────────────┘
```
