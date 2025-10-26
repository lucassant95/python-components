# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-10-26

### Changed

- **BREAKING**: Changed start method call from the Component interface to receive the system instance instead of
  individual dependencies. This is to support more complex initialization scenarios.

### Added

- Added `get_component` method to `System` class for retrieving components by key from the system-map.

## [0.2.0] - 2025-10-26

### Changed

- **BREAKING**: Renamed package directory from `src/` to `python_components/` to avoid import conflicts
- **BREAKING**: Updated import paths: use `from python_components import Component, System` instead of
  `from src.component import Component`
- Updated all internal imports to use `python_components.*` namespace
- Updated documentation with new import examples
- Updated test configuration to point to new package location

### Added

- Created proper `__init__.py` with `__all__` exports for cleaner imports
- Added `MIGRATION.md` guide for upgrading from 0.1.0
- Added `CHANGELOG.md` for tracking changes

### Fixed

- Fixed import conflicts for users with `src/` directory structure in their projects
- Package now follows Python packaging best practices

## [0.1.0] - 2025-10-26

### Added

- Initial release
- `Component` abstract base class with lifecycle management
- `System` class for dependency management and orchestration
- Automatic dependency resolution using topological sorting
- Circular dependency detection
- Comprehensive test suite
- Full documentation and examples

[Unreleased]: https://github.com/yourusername/python-components/compare/v0.1.0...HEAD

[0.1.0]: https://github.com/yourusername/python-components/releases/tag/v0.1.0

