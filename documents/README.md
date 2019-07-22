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
    - [Description of IFD](#Description-of-IFD)
    - [Format of IFD](#Format-of-IFD)
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

If you want to remove your project without removing if-maker, you can run `python3 ifm.py clear` to remove the folders and files generated by if-maker.

## IFD - Interactive Fiction Data

### Description of IFD

IFD file is designed to store object or item data of the game. It is based on [YAML](https://yaml.org/). Actually, every IFD file is a valid YAML file, the file name extension IFD is used only for VSCode extension [ifd-highlighter](https://marketplace.visualstudio.com/items?itemName=DiscreteTom.ifd-highlighter) to recognize that this file is an interactive fiction data file.

IFD files are stored in `_items` folder. The entry file is the `_items/index.ifd`. You can write all your items in the index file, or you can write them in other IFD files and `include` then in index file.

### Format of IFD

Every IFD file can include other IFD files. Remember that recursive including is invalid.

```yaml
include:
  - filename
```

Every IFD file can contain many items, every item has these attributes:
- id - The identifier in your [scripts](#Scripts). You can reference an item using `items['itemID']`. See [Built-in Content](#Built-in-Content).
- name - The name is used to be displayed on [shell](#Shell). You can change the name of any item during the game, but do not change its id.
- description
- onMount & onUnmount - Python scripts that will be executed when this item is [mounted & unmounted](#Mount--Unmount) to [shell](#Shell). The `|` and `^` are not the part of python code. Please see the examples below to make sure your indentation of code is right.
- actions - Every action has two attributes: name and code. The code are the same format as the code in onMount & onUnmount. See [Action](#Action).
- classes - Each item can belong to 0 or many classes. See [Classes](#Classes).
- data - Custom data.

```yaml
itemID:
  id: 'itemID' # Auto-generated. you don't have to write this attribute in your IFD file
  name: 'itemName'
  description: ''
  onMount: |
    # python code here
    ^
  onUnmount: |
    # here is an example about indentation
    while input('please input "1"') != '1':
      print('you are wrong')
    ^
  actions:
    - name: 'word1 word2'
      code: |
        # python code here
        ^
  classes: 
    - 'className'
  data:
    customData
```

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

### Tab Completion

TODO

## Others

### Language Support

We hope the games made by if-maker can support any language in the world. Now we have tested games in English and Chinese and they work well.