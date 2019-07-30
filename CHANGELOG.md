# CHANGELOG

## [Unreleased]

### Added

- Modules can contain a `config.yml` file.
- Action names can contain `[]` to match any string.
- Function `parse` can handle exit command now.

### Fixed

- Function `run` can not remove the indent of code.
- Clear input buffer after printing story.
- Function `make` can not generate the right item file.
- Function `load` will break data consistency.
- Pressing `ESC` can not skip complex stories with many tags.
- Function `printItemList` went wrong if the size of item list is bigger than two.

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