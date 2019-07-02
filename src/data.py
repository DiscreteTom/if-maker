'''
- `config` to access config variables
- `items` to access items
- `game` to access global variables
- `completer` to add user defined words
- `findItem(itemName)` to get item id
- `save/load(fileName)` to save/mount game progress
'''

from refdict import refdict
import json

config = refdict({})
items = refdict({})
game = refdict({})
completer = set()

def findItem(itemName: str):
	'''
	return item ID. if item ID is not found, return None
	'''
	global items
	for itemID in items:
		if items[itemID]["name"] == itemName:
			return itemID
	return None

def save(fileName: str):
	'''
	save game progress to `fileName`
	'''
	import shell
	global items, config, game, completer
	f = open(fileName, 'w', encoding='utf-8')
	result = {
		'items': str(items),
		'config': str(config),
		'game': str(game),
		'completer': str(completer),
		'shell': str(shell.loadedItems)
	}
	json.dump(result, f)
	f.close()

def load(fileName = '') -> None:
	'''
	load game progress from `fileName`

	if `fileName` is not given, load data from default location
	'''
	import shell
	global items, config, game, completer
	if len(fileName):
		# load data from SAVE file
		f = open(fileName, encoding='utf-8')
		d = json.load(f)
		completer = eval(d['completer'])
		items = eval(d['items'])
		config = eval(d['config'])
		game = eval(d['game'])
		shell.loadedItems = eval(d['shell'])
		f.close()
		return

	# ======================== load file from default location
	# load config
	f = open('output/config', encoding='utf-8')
	config = refdict(json.load(f))
	f.close()
	# load items
	f = open('output/items', encoding='utf-8')
	items = refdict(json.load(f))
	f.close()
	# user defined global data
	game = refdict({})
	completer = set()

load()