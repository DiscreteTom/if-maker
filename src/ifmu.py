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