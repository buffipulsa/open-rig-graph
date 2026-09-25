# Changelog

All notable changes to OpenRigGraph are documented here.

## [0.1.0] - 2026-09-22

### Added

- Initial `uv`-managed Python package layout.
- Immutable TRS `Transform` values with quaternion rotation support.
- Pure transform composition for FK evaluation.
- Stable semantic entities with optional parent relationships.
- Recursive and batch world-transform evaluation.
- Explicit validation for cycles, missing parents, and unknown entities.
- Automated tests covering root evaluation, FK translation, rotation, scale,
  and hierarchy errors.
- MIT license.

### Documentation

- Added README guidance for the current FK experiment and development setup.
- Added API and module docstrings for the package, entities, transforms, and
  evaluation functions.
