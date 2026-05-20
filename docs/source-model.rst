Source model
============

Canonical source
----------------

The source of truth is the fragment tree under ``archledger_dir``:

- ``sections/`` for the major arc42 chapter skeleton
- ``records/`` for individual architecture facts

Fragments contain YAML front matter and a body in the configured dialect.

Traceability
------------

Use ``source_refs`` when fragments describe real files or directories.
Directory refs must end with ``/`` and must exist in the workspace.

Generated output
----------------

Files under ``.archledger/build/`` are derived artifacts and should not be edited
as source.
