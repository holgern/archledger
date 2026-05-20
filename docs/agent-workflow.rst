Agent workflow
==============

Recommended loop
----------------

1. Run ``archledger --json where``.
2. Run ``archledger --json changed`` before broad architecture refreshes.
3. Run ``archledger --json read --include-body --include-draft``.
4. Edit only the fragment files under ``sections/`` and ``records/``.
5. Run ``archledger --json check``.
6. Build only when the user needs an exported artifact.
7. Run ``archledger --json snapshot --reason after-archledger-update`` after the updates have been validated.

Rules
-----

- Treat the fragment tree as the source of truth.
- Do not edit ``.archledger/build`` output as source.
- Add ``source_refs`` when a fragment describes concrete implementation artifacts.
