# if-maker

## 概述

if-maker是一个基于python编写的文本游戏(Text-Based Game)引擎，目标是能够较为轻易地构造像zork一样优秀的文本游戏。游戏制作者仅需要提供必要的数据和简单的逻辑就可以制作出文本游戏，而不需要担心过多的游戏框架的问题

## 一些概念

- 玩家player - 玩游戏的人
- shell - 和玩家进行交互的用户界面
- 主角hero - 玩家控制的角色
- 物体item - 指可与主角交互的对象。物体包含以下属性：
  - ID
  - 名字name
  - 介绍description
  - 所属的类classes
  - 支持的交互actions
  - 被装载到shell的时候会触发的事件onMount
  - 从shell中卸载的时候会触发的事件onUnmount
  - 其他数据data
- 装载与卸载mount&unmount - 主角只能触发被装载到shell的物体的事件
- 类 - 一些物体可能会有相同的属性，可以把这些属性抽象成一个类。物体也可以不属于任何类

## 新建项目

### 新建项目命令与目录结构

使用命令`ifm new`可以创建一个新的项目，也可以直接使用命令`ifm new projectName`创建一个名为projectName的项目

如果不出意外，执行上述命令的文件夹应该会有如下的目录结构：

```
│   ifm.exe
│   _config.yml
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

其中`ifm.exe`为if-maker的可执行文件，`_config.yml`保存了系统配置信息，文件夹`_items`内的文件保存了游戏中会和主角交互的物体，文件夹`_classes`内的文件保存了物体的类，`_modules`保存了一些模块，`_scripts`文件夹内的文件保存了游戏中可能被调用的公共函数，`_stories`文件夹内的文件保存了游戏的剧情文本。

### _config.yml

保存了系统配置，能够使用的项及其默认值如下：

```yml
project:
  name: 'untitled project' # 项目名称
system: 
  shell: 
    prefix: '>' # 命令行前缀
    exitCmd: 'exit' # 退出指令
    errorMsg: 'invalid command' # 输入无效指令时的错误信息
  print: 
    interval: 0.02 # 输出时逐字符输出的间隔
    indent: '' # 输出前缀
    skip': True # 是否跳过输出（即不使用逐字符输出）
  story: 
    first: '0' # 第一段剧情文本的ID
    skip: False # 输出剧情文本时是否跳过（即不使用逐字符输出）
  entry: 'ifmain' # 入口函数，即游戏启动时调用的第一个函数
make: 
  modules: [] # 构建时使用的模块
  globalClasses: [] # 全局类。所有item都会包含这些类
debug: [] # 调试输出，值可以包括'run', 'mount', 'unmount', 'parse'
data: # 自定义配置数据
```

### _items

此文件夹包含了物体数据文件。其中index.ifd文件为入口，系统会处理此文件和它include的文件

ifd文件本质上为yaml文件，其中所有物体对象的数据格式为：

```yml
itemID:
  name: 'itemName'
  description: ''
  onMount: |
    # python code here
    ^
  onUnmount: |
    # python code here
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



### _classes

TODO

### _modules

TODO

### _scripts

TODO

### _stories

TODO

## 清除项目
TODO

## 构建项目
TODO

## 运行项目
TODO

## 打包发布
TODO

## ifd文件参考文档
TODO

## ift文件参考文档
TODO
