# if-maker

<details>
<summary>Table of Contents</summary>

- [if-maker](#if-maker)
  - [Description](#description)
    - [What is if-maker](#what-is-if-maker)
    - [Prerequisites](#prerequisites)
  - [Install](#install)
    - [Dependency](#dependency)
    - [Download](#download)
    - [Tools](#tools)
  - [Project Management](#project-management)
    - [Create a project](#create-a-project)
    - [Config your project](#config-your-project)
    - [Compile your project](#compile-your-project)
    - [Run your project](#run-your-project)
    - [Debug your project](#debug-your-project)
    - [Release your project](#release-your-project)
    - [Clear your project](#clear-your-project)
  - [IFD - Interactive Fiction Data](#ifd---interactive-fiction-data)
    - [Description of IFD](#description-of-ifd)
    - [Format of IFD](#format-of-ifd)
    - [Items](#items)
    - [Classes](#classes)
    - [Modules](#modules)
    - [Value Reference](#value-reference)
    - [Self-Reference](#self-reference)
    - [IFD Merging Rules](#ifd-merging-rules)
  - [IFT - Interactive Fiction Text](#ift---interactive-fiction-text)
    - [Description of IFT](#description-of-ift)
    - [Supported Elements](#supported-elements)
    - [Value Reference in IFT](#value-reference-in-ift)
    - [Printing Story](#printing-story)
  - [Scripts](#scripts)
    - [Description of Scripts](#description-of-scripts)
    - [Built-in Content](#built-in-content)
  - [Shell](#shell)
    - [Mount & Unmount](#mount--unmount)
    - [Action](#action)
    - [Tab Completion](#tab-completion)
  - [Others](#others)
    - [Manage Global Data](#manage-global-data)
    - [Language Support](#language-support)

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
- Usage of [refdict](https://pypi.org/project/refdict/).

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
    skip: True # if false, print strings char by char, 
    interval: 0.02 # the time interval of chars when printing. become effective when system.print.skip is false. using second as unit
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

Items of your project are stored in `_items` folder. The entry file is the `_items/index.ifd`. You can write all your items in the index file, or you can write them in other IFD files in `_items` folder and `include` then in index file.

Usually items are the kind of data which can interact with player because they have the `actions` attribute. Also you can store some global data as an item. See [Manage Global Data](#Manage-Global-Data)

Item's id can not be `include` because this key is preserved in IFD files to include other IFD files.

### Classes

If some items have some attributes in common, you can abstract those attributes in a class. For example, if you want all items to have an [action](#Action) named `watch this`, you can abstract a class as follows:

```yaml
watchable:
  data:
    _watchable_times: 0
  actions:
    - name: 'watch this'
      code: |
        printf(this['description'])
        this['data._watchable_times'] += 1
        printf('you have watched this item', this['data._watchable_times'], 'times')
        ^
```

Then you can use this class in your items.

Classes of your project are stored in `_classes` folder. The entry file is `_classes/index.ifd`. You can `include` other class files in index file.

Just like items, every class also has an attribute called `classes`, so every class can contain other classes. When merging two classes, the current class is the `higher`, and the contained class is `lower`. See [IFD Merging Rules](#Merge-Rules).

When merging an item and it's classes, the items is the `higher` and the classes are the `lower`. See [IFD Merging Rules](#Merge-Rules).

To avoid conflicts, attributes of the `data` attribute in class should be well named. In the above example we use `_className_varName` as the naming rules.

### Modules

Modules are project-independent classes, items and configs. You can reuse them in many projects.

Modules are stored in `_modules` folder as sub-folders. Every module contains an `item.ifd` file, a `classes.ifd` file, and a `config.yml` file. For example, if we have a module named `test`, the folder structure of `_modules` should be like this:

```
_modules
└───test
        classes.ifd
        items.ifd
        config.yml
```

You have to add module names in `config['make.modules']` to activate these modules.

When merging items and classes, the project items and classes are the `higher` and the module items and classes are the `lower`. See [IFD Merging Rules](#Merging-Rules).

When merging config, the merging rules of config are as follows:

```yaml
project:
  name: '' # use project's if project's is not empty
system:
  shell:
    prefix: '>' # use project's if project's is not empty
    exitCmd: 'exit' # use project's if project's is not empty
    errorMsg: 'invalid command' # use project's if project's is not empty
  print:
    skip: True # use project's if project's is given
    interval: 0.02 # use project's if project's is given
    indent: '' # use project's if project's is not empty
  story:
    first: '0' # use project's if project's is not empty
    skip: False # use project's if project's is given
  entry: 'ifmain' # use project's if project's is not empty
make: 
  modules: [] # merge
  globalClasses: [] # merge
debug: [] # merge
data: # merge, consider conflicts, use project's
```

### Value Reference

Because the variable [`item`](#built-in-content) is a [refdict](https://pypi.org/project/refdict/), you can reference another item using a string starts with `@`. Here is an example:

```yaml
player:
  name: 'DiscreteTom'
  data:
    items:
      - '@apple'
      - '@red-potion'
    weapon: '@sword'
    attack: '@player.weapon.attack'
    me: '@player'

apple:
  name: 'apple'
  description: 'restore your health by 10%'

red-potion:
  name: 'red potion'
  description: 'restore your health by 20%'

sword:
  name: 'sword'
  description: 'A nice sword'
  data:
    attack: 123
    value: 50
```

### Self-Reference

You can use the keyword this in action's `name` and `code` as a reference of current item. In `action.name`, `this` will be replaced by the item's `name`. In `action.code`, `this` will be replaced by `items('itemID')`. Here is an example:

```yaml
NPC-1:
  name: 'DiscreteTom'
  description: 'The developer of if-maker'
  data:
    repositories:
      - 'if-maker'
  action:
    - name: 'who is this'
      code: |
        printf(this['name'])
        printf(this['description'])
        printf('repositories:')
        printItemList(this['data.repositories'])
        ^
```

During the game, when you input `who is DiscreteTom`, if this item is [mounted](#mount--unmount) to [shell](#shell) and there is no naming conflicts, the action `who is this` will be triggered.

### IFD Merging Rules

When we want to merge two IFD items, we name them `higher` and `lower`. Here is the merging rules:

```python
result = {
'name': '', # use higher's if higher's is not empty
'description': '', # use higher's if higher's is not empty
'actions': [ # merge, ignore conflict, lower's after higher's
	{
		'name': '',
		'code': ''
	}
],
'onMount': '', # merge, ignore conflict, higher's after lower's
'onUnmount': '', # merge, ignore conflict, higher's after lower's
'data': {} # merge, consider conflict, use higher's
}
```

## IFT - Interactive Fiction Text

### Description of IFT

IFT files are based on XML, but IFT files are not valid XML files. To make it simpler than XML, we remove the XML header label and the root element, and add an include rule.

In [VSCode](https://code.visualstudio.com/), we developed an extension [ift-highlighter](https://marketplace.visualstudio.com/items?itemName=DiscreteTom.ift-highlighter) to optimize your developing experience.

Every IFT file consists many **stories**. Every story has an ID, you can print your story by using `printStory`. See [Built-in Content](#Built-in-Content).

The stories are stored in `_stories` folder. The `_stories/index.ift` is the entry file. You can include other IFT files by adding `#include filename` at the top of IFT files. The `filename` should not contain blank characters.

### Supported Elements

- `<story id="">content</story>` - Story element. The basic unit of IFT file.
- `<if condition="">content</if>` - The content will take effect if `condition` returns true.
- `<while condition="">content</while>` - The content will take effect while `condition` returns true.
- `<code>content</code>` - Run `content` as python code.
- `<input prompt="">dest</input>` - Get user input and store it in `dest`. You can only access `dest` in the same context of this `input` element.

### Value Reference in IFT

In IFT file, you can use `{{ value }}` to reference a value. Here is an example:

```xml
<story id="0">
  Hello everyone, my name is {{ items['player.name'] }}.
</story>
```

### Printing Story

If `config['system.story.skip']` is false, the story will be printed line by line. The leading blank characters will be removed. Here is an example:

```xml
<story id="0">
  Hello, world.
  <if condition="True">
    There is no indentation in this line.
  </if>
</story>
```

If you print this story, the result is:

```
Hello, world.
There is no indentation in this line.
```

If you want to set indentation of your story, you can use `config['system.print.indent']`:

```xml
<story id="0">
  Hello, world.
  <if condition="True">
    <code>
      game['tmp'] = config['system.print.indent']
      config['system.print.indent'] = '    '
    </code>
    There are 4 spaced at the beginning of this line.
    <code>
      config['system.print.indent'] = game['tmp']
    </code>
  </if>
</story>
```

If you print this story, the result is:

```
Hello world.
    There are 4 spaced at the beginning of this line.
```

## Scripts

### Description of Scripts

You can run any python code in if-maker.

All your scripts should be stored in `_scripts` folder. After you [creating a new project](#Create-a-project), their will be 2 files in `_scripts` folder:
- `ifmu.py`
- `main.py`

The `ifmu.py` contains the code completion information of [built-in content](#Built-in-Content) of if-maker, so it will be ignored when compiling your project. The `main.py` contains the default entry function `ifmain`. You can change the default entry function in `config['system.entry']`, see [Config your project](#Config-your-project).

There is no entry file. All files in `_scripts` folder except `ifmu.py` will be merged into an output script file. The output script will remove all `from ifmu import *`.

In script files you can do anything you want to do. You can also define classes there.

If you want to call something in these scripts, for example you write a function named `func`, then you can directly call it in IFT and IFD.

### Built-in Content

You can find all information of built-in content in `ifmu.py`.

<details>
<summary>ifmu.py</summary>

```python
from refdict import refdict

def printf(*values: str, **kwargs):
	'''
	`printf(values, ..., skip = config['system.print.skip'], sep = ' ', end = '\\n', indent = config['system.print.indent'])`

	replace variables in `{{}}` with its value
	'''

def printStory(story_id: str) -> bool:
	'''
	print the story whose id is `story_id`

	return False if story_id is not found in story file
	'''

def printItemList(l: list, skip = True, indent = '- ', sep = '\n', end = '\n'):
	'''
	`l` should be a list of item id, print those names
	'''

def parse(cmd: str):
	'''
	parse a command
	'''

def loadedItems() -> list:
	'''
	return a list of item id which are loaded in shell
	'''

def mount(*items):
	'''
	mount `items` to shell so that shell can parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''

def unmount(*items):
	'''
	unmount `items` from shell so that shell can not parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''

items = refdict({})
config = refdict({})
game = refdict({}) # store user defined global data
completer = set()

def findItem(itemName: str):
	'''
	return item ID. if item ID is not found, return None
	'''

def save(fileName: str):
	'''
	save game progress to `fileName`
	'''

def load(fileName = '') -> None:
	'''
	load game progress from `fileName`

	if `fileName` is not given, load data from default location
	'''

def start():
	'''
	start project by calling `config['system.entry']`
	'''

def newGame():
	'''
	start a new game, print story: `config['system.story.first']`, load data and loop
	'''

def loop():
	'''
	enable shell
	'''

def run(code: str, params = {}):
	'''
	run `code` in ifm environment
	'''
```

</details>

## Shell

### Mount & Unmount

Not every item can interact with the player. Only those which are **mounted** to shell can interact with the player. If an item can not interact with the player at some moment, it should be **unmounted** from shell.

This is to avoid naming conflict, optimize command parsing and tab completion. Here is an example of using mount & unmount to achieve location change of the player:

```yaml
# _items/index.ifd
player:
  data:
    location: '@home'
  actions:
    - name: 'where am i'
      code: |
        printf(this['data.location.name'])
        printf(this['data.location.description'])
        ^
    - name: 'to (where)'
      code: |
        if ('@' + where) in this['data.location.data.neighbors']:
          unmount(this['data.location'])
          this['data.location'] = '@' + where
          mount(this['data.location'])
        ^

home:
  name: 'home'
  description: 'your home'
  data:
    neighbors:
      - '@shop'
    contains:
      - '@home-bed'
      - '@home-table'
  onMount: |
    mount(this['data.contains'])
    ^
  onUnmount: |
    unmount(this['data.contains'])
    ^

shop:
  name: 'shop'
  description: 'a nearby shop'
  data:
    neighbors:
      - '@home'
    contains:
      - '@bottle-water'
      - '@food'
  onMount: |
    mount(this['data.contains'])
    ^
  onUnmount: |
    unmount(this['data.contains'])
    ^
```

The `onMount` and `onUnmount` attribute are hooks of mount and unmount action. The content of `onMount` and `onUnmount` is python code and will be executed after mount and unmount.

### Action

Every action has two attributes: `name` and `code`.

The keyword `this` in `name` will stand for the item's name. The variable `this` in `code` will stand for the item itself. See [Sefl-Reference](#self-reference).

If a command contains some items' name and these items are not mounted to shell, you can use `(param: className)` in `name` to catch it. The `param` will be assigned to the matched item's id. Here is an example:

```yaml
player:
  data:
    location: '@home'
  actions:
    - name: 'to (where: location)'
      code: |
        if ('@' + where) in this['data.location.data.neighbors']:
          unmount(this['data.location'])
          this['data.location'] = '@' + where
          mount(this['data.location'])
        ^
home:
  classes:
    - 'location'
  data:
    neighbors:
      - '@shop'
shop:
  classes:
    - 'location'
  data:
    neighbors:
      - '@home'
```

### Tab Completion

Pressing `tab` will trigger the tab completion of shell. Shell will first look for words in the variable [`completer`](#built-in-content), then in the mounted items in shell.

## Others

### Manage Global Data

There are 3 places to store global data:
- In `config['data']`. See [Config your project](#Config-your-project).
- In `items`. See [Items](#Items)
- In `game`. See [Built-in Content](#Built-in-Content)

Here is a suggestion about where to put your global data:
1. If the data is generated during the game, store it in `game` because the content of `game` is generated during the game and you can not edit `game` when developing your project.
2. If the data is defined when developing your project, and it's project-independent, maybe you can abstract it as a part of [module](#Modules) so you can reuse it in other projects.
3. Otherwise, store these data in an item is fine.

### Language Support

We hope the games made by if-maker can support any language in the world. Now we have tested games in English and Chinese and they work well.