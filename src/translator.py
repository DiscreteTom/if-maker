from shell import mount, unmount, parse, loadedItems
from data import config, items, game, completer, findItem, save, load
from story import print, printStory, printItemList
from controller import start, newGame, loop

def run(code: str, params = {}):
	if 'debug.run' in config:
		print('debug.run: running', code, 'params:', params)
	result = None
	# construct env
	result = exec(code)
	return result
