# CHANGELOG

## [Unreleased]

### Added

- Modules can contain a `config.yml` file.
- Action names can contain `[]` to match any string.

### Fixed

- Function `run` can not remove the indent of code.
- Clear input buffer after printing story.
- Function `make` can not generate right item file.

## [v0.1.1] - 2019-07-18

### Added

- Support for non-windows platform. 

## [v0.1.0] - 2019-07-16

### Added

- Command `ifm install` to install.
- Command `ifm new` to create a new project.
- Command `ifm make` to compile project.
- Command `ifm run` to run project.
- Command `ifm debug` to compile and run project.
- Command `ifm clear` to clear project.