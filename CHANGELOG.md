# Changelog

All notable changes to OpenRigGraph are documented here.

## [Unreleased]

### Added

- Added NumPy as a runtime dependency for numerical rig evaluation.
- Added a NumPy-based aim rotation operator with validation for undefined aim
  directions.
- Added automated aim operator tests.
- Added a GitHub Actions workflow that runs the FK and aim test suites on
  pushes and pull requests.
- Added world-space evaluation of semantic aim constraints.
- Added explicit rotation composition for parent/local rotation workflows.
- Added Ruff as a development dependency and required CI linting.
- Clarified NumPy array and scalar types in aim evaluation.

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
