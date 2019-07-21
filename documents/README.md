# if-maker

<details>
<summary>Table of Contents</summary>

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
    - [Config your project](#Config-your-project)
    - [Compile your project](#Compile-your-project)
    - [Run your project](#Run-your-project)
    - [Debug your project](#Debug-your-project)
    - [Release your project](#Release-your-project)
    - [Clear your project](#Clear-your-project)
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

</details>

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
- Basic data format of YAML file.
- Basic data format of XML file.

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

### Config your project

The file `_config.yml` in your project root folder contains the config information of your project. The items and their default values are as follows:

```yaml
project:
  name: 'untitled project'
system:
  shell:
    prefix: '>'
    exitCmd: 'exit'
    errorMsg: 'invalid command' # will be printed if command can not be parsed
  print: # will influence the built-in function `printf`
    skip: True # if false, print strings char by char
    interval: 0.02 # become effective when system.print.skip is false. using second as unit
    indent: ''
  story:
    first: '0' # ID of the first story
    skip: False # if false, print stories char by char
  entry: 'ifmain' # entry function
make: # effective only at `ifm make`
  modules: [] # activated modules
  globalClasses: [] # all items will contain these classes
debug: [] # debug these functions: ['run', 'mount', 'unmount', 'parse']
data: # user defined config data
```

Configs of your project can be changed during your game. You can access it by using the variable `config` in your [scripts](#Scripts).

The variable `config` is a [refdict](https://pypi.org/project/refdict/) object, so you can use a string as a chain key to get or set value.

For example, if you want to set the value of `config['system']['shell']['prefix']` to `'player>>'`, you can just write `config['system.shell.prefix'] = 'player>>'`.

### Compile your project

Run `python3 ifm.py make` to compile your project. After compiling, there should be an `output` folder in your `src` folder.

These 4 files should be generated in `output` folder:

- `config`
- `items`
- `story`
- `__init__.py`

>Command `python3 ifm.py debug` will also compile your project, see [Debug your project](#Debug-your-project).

### Run your project

Run `python3 ifm.py run` to run your project. By default, if-maker will call the `ifmain` function in `_scripts/main.py`. You can change your entry function in [`_config.yml`](#Config-your-project).

>Command `python3 ifm.py debug` will also run your project, see [Debug your project](#Debug-your-project).

### Debug your project

>This feature is under development.

Run `python3 ifm.py debug` will [compile](#Compile-your-project) your project and then [run](#Run-your-project) your project in debug mode.

In debug mode, built-in functions in `config['debug']` will output debug message. See `config` in [Config your project](#Config-your-project).

### Release your project

>This feature is under development. You can use [PyInstaller](https://pypi.org/project/PyInstaller/) to realize this feature by yourself.

Run `python3 ifm.py release` will generate an executable release of your project.

### Clear your project

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

## Scripts

### Function Call

TODO

### Built-in Content

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