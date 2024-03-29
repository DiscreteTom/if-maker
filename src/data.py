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

def findItem(itemName: str, className = ''):
	'''
	return item ID. if item ID is not found, return None

	`className` is a class name
	'''
	global items
	for itemID in items:
		if items[itemID]["name"] == itemName and className in items[itemID]['classes']:
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
		'shell': str(shell.itemActions)
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
		# reload refdict
		items.load(eval(d['items']))
		config.load(eval(d['config']))
		game.load(eval(d['game']))
		# reload set
		completer.clear()
		t = eval(d['completer'])
		for value in t:
			completer.add(value)
		# reload dict
		shell.itemActions.clear()
		t = eval(d['shell'])
		for key in t:
			shell.itemActions[key] = t[key]
		f.close()
		return

	# ======================== load file from default location
	# load config
	f = open('output/config', encoding='utf-8')
	config.load(json.load(f))
	f.close()
	# load items
	f = open('output/items', encoding='utf-8')
	items.load(json.load(f))
	f.close()
	# user defined global data
	game.load({})
	completer.clear()

load()