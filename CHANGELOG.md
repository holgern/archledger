# Changelog

All notable changes to `archledger` will be documented in this file.

## Unreleased

### Added

- GitHub Actions CI for Python 3.10 through 3.13, including package build, metadata checks, and installed-wheel smoke coverage.
- Optional real-tool converter integration tests for Pandoc and Asciidoctor-backed builds.
- Dedicated internal modules for source-ref validation, content checks, CLI payload formatting, and converter planning.
- Maintainer release-process documentation and clearer source-tracking workflow guidance.

### Changed

- Packaging now relies on `pyproject.toml` build metadata only; the legacy `setup.py` entrypoint has been removed.
- README and docs now explain release status, commit policy for `.archledger/` contents, and practical `source_refs`/drift-update workflows.

### Fixed

- `config_version = true` is now rejected instead of being accepted as integer `1`.
- `storage.yaml` counters such as `next_numbers.requirement: true` are now rejected instead of being accepted as integer counters.
- Source-ref and source-state path validation now consistently enforce POSIX-relative path rules.
