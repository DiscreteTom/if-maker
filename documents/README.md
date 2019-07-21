# if-maker

- [if-maker](#if-maker)
  - [Description](#Description)
    - [Prerequisites](#Prerequisites)
  - [Install](#Install)
  - [Project Management](#Project-Management)
    - [Create a project](#Create-a-project)
    - [Compile your project](#Compile-your-project)
    - [Run your project](#Run-your-project)
    - [Debug your project](#Debug-your-project)
  - [Interactive Fiction Data(ifd)](#Interactive-Fiction-Dataifd)
    - [Items](#Items)
    - [Classes](#Classes)
    - [Modules](#Modules)
  - [Interactive Fiction Text(ift)](#Interactive-Fiction-Textift)
  - [Shell](#Shell)
    - [Mount & Unmount](#Mount--Unmount)
    - [OnMount & OnUnmount](#OnMount--OnUnmount)
    - [Tab Completion](#Tab-Completion)

## Description

TODO

### Prerequisites

Though if-maker can help you to build a text-based game, you still have to know:
- Basic programming with python3(built-in data structure, control flow, function).
- Basic data format of YAML file(ifd file is based on YAML file).
- Basic data format of XML file(ift file is based on XML file).

## Install

- Download `ifm.py` in the root folder of the repository, then run `python3 ifm.py install`(network access is needed).
- Or, download `ifm.py` and `src/*` in the root folder of the repository.

We recommend to edit the source code of your project with [VSCode](https://code.visualstudio.com/).

Also we developed two extensions for VSCode to edit `ifd` and `ift` file more effectively, just search `ifd-highlighter` and `ift-highlighter` in the extension window of VSCode to install them.

## Project Management

### Create a project

Use command `python3 ifm.py new` to create a new project, or use `python3 ifm.py new projectName` to create a project called `projectName`.

If everything is OK, your folder structure will be like this:

```
│   ifm.py
│   _config.yml
│
├───src
│       controller.py
│       data.py
│       ifmu.py
│       output_header.py
│       shell.py
│       story.py
│       translator.py
│
├───_classes
│       index.ifd
│
├───_items
│       index.ifd
│
├───_modules
├───_scripts
│       ifmu.py
│       main.py
│
└───_stories
        index.ift
```

### Compile your project

Run `python3 ifm.py make` to compile your project. After compiling, there should be an `output` folder in your `src` folder.

These 4 files should be generated in `output` folder:

- `config`
- `items`
- `story`
- `__init__.py`

Command `python3 ifm.py debug` will also compile your project, see [Debug your project](#Debug-your-project).

### Run your project

TODO

### Debug your project

TODO

## IFD - Interactive Fiction Data

TODO

### Items

TODO

### Classes

TODO

### Modules

TODO

## IFT - Interactive Fiction Text

TODO

## Shell

### Action

TODO

### Mount & Unmount

TODO

### OnMount & OnUnmount

TODO

### Tab Completion

TODO


