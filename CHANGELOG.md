# CHANGELOG

## [Unreleased]

### Added

- Modules can contain scripts. Just name it `scripts.py` in module folders.
- Include many other IFT files in one line in IFT file just like `#include file1 file2 file3`

### Changed

- Params in the name of actions will be passed as the item itself rather than the item's id.

## [v0.1.2] - 2019-08-01

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
- Function `make` can not merge items' code in `onMount`/`unMount`.
- Function `make` can not merge items' classes correctly.

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