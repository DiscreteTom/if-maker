from refdict import refdict

this = refdict({})

def print(*values: str, **kwargs):
	'''
	`print(values, ..., skip = True, sep = ' ', end = '\\n', indent = '')`

	print `values` as `str`, parse `{}` commands in `values`
	'''

def printStory(story_id) -> bool:
	'''
	`story_id` can be a `str` or an `int`

	return `False` if story is not found
	'''

def printItemList(l: list, **kwargs):
	'''
	`l` should be a list of item id

	kwargs: `skip = True`, `indent = '- '`
	'''

def parse(cmd: str):
	'''
	let shell parse `cmd`
	'''

def load(*items):
	'''
	load `items` to shell so that shell can parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''

def unload(*items):
	'''
	unload `items` from shell so that shell can not parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''

def run(code: str, params={}):
	'''
	run `code` with `params`

	running environment contains all members in ifmu.py
	'''

items = refdict({})
config = refdict({})
game = refdict({}) # store user defined global data

def findItem(itenName: str):
	'''return item ID'''