# if-maker

- [if-maker](#if-maker)
  - [Description](#Description)
    - [What is if-maker](#What-is-if-maker)
    - [Prerequisites](#Prerequisites)
  - [Install](#Install)
    - [Dependency](#Dependency)
    - [Download](#Download)
    - [Tools](#Tools)
  - [Project Management](#Project-Management)
    - [Create a project](#Create-a-project)
    - [Compile your project](#Compile-your-project)
    - [Run your project](#Run-your-project)
    - [Debug your project](#Debug-your-project)
  - [IFD - Interactive Fiction Data](#IFD---Interactive-Fiction-Data)
    - [Items](#Items)
    - [Classes](#Classes)
    - [Modules](#Modules)
  - [IFT - Interactive Fiction Text](#IFT---Interactive-Fiction-Text)
  - [Scripts](#Scripts)
    - [Function Call](#Function-Call)
    - [Built-in Content](#Built-in-Content)
  - [Shell](#Shell)
    - [Action](#Action)
    - [Mount & Unmount](#Mount--Unmount)
    - [OnMount & OnUnmount](#OnMount--OnUnmount)
    - [Tab Completion](#Tab-Completion)
  - [Others](#Others)
    - [Language Support](#Language-Support)

## Description

### What is if-maker

The full name of if-maker is **[Interactive Fiction](https://en.wikipedia.org/wiki/Interactive_fiction) Maker**. Obviously it is designed to build interactive fiction games or text-based games just like [zork](https://en.wikipedia.org/wiki/Zork).

The games built by if-maker have NO GUI, just CLI. Players have to type command in the [shell](#Shell) to interact with our games. It doesn't sound very attractive to many players nowadays, but it will be fun to explore a game just with your imagination.

To make the developing process easier, developers just need to provide necessary [data](#IFD---Interactive-Fiction-Data), [stories](#IFT---Interactive-Fiction-Text) and [control logics](#Scripts) for if-maker, and if-maker will do the rest of all jobs, including:

- Command parsing
- Tab completion
- Save & Load game data
- Build executable release
- ...

### Prerequisites

Though if-maker can help you to build a text-based game, you still have to know:
- Basic programming with python3(built-in data structure, control flow, function).
- Basic data format of YAML file(ifd file is based on YAML file).
- Basic data format of XML file(ift file is based on XML file).

## Install

### Dependency

- [PyYAML](https://pypi.org/project/PyYAML/)
- [refdict](https://pypi.org/project/refdict/)
- [keyboard](https://pypi.org/project/keyboard/)
- [pyreadline](https://pypi.org/project/pyreadline/)

### Download

- Download [`ifm.py`](https://raw.githubusercontent.com/DiscreteTom/if-maker/master/ifm.py) in the root folder of the repository, then run `python3 ifm.py install`(network access is needed).
- Or, download `ifm.py` and `src/*` in the root folder of the repository.

### Tools

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

## Control Logics

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

## Others

### Language Support

We hope the games made by if-maker can support any language in the world. Now we have tested games in English and Chinese and they work well.