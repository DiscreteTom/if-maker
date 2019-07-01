from shell import shell
from data import data
from story import story
import controller

globalData = {}

def run(code: str, params = {}):
	code = 'from output import *\n' + code
	if 'debug.run' in data.config:
		print('debug.run: running', code, 'params:', params)
	result = None
	# construct env
	result = exec(code, globalData, params)
	return result

globalData = {
	'mount': shell.mount,
	'unmount': shell.unmount,
	'parse': shell.parse,
	'print': story.print,
	'printStory': story.printStory,
	'printItemList': story.printItemList,
	'config': data.config,
	'items': data.items,
	'game': data.game,
	'findItem': data.findItem,
	'run': run,
	'loadedItems': shell.loadedItems,
	'save': data.save,
	'load': data.load,
	'newGame': controller.newGame,
	'loop': controller.loop,
}