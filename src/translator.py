from shell import shell
from data import data
from story import story

globalData = {}

def run(code: str, params = {}):
	if 'debug.run' in data.config:
		print('debug.run: running', code, 'params:', params)
	result = None
	# construct env
	result = exec(code, globalData, params)
	return result

globalData['load'] = shell.load
globalData['unload'] = shell.unload
globalData['parse'] = shell.parse
globalData['print'] = story.print
globalData['printStory'] = story.printStory
globalData['printItemList'] = story.printItemList
globalData['config'] = data.config
globalData['items'] = data.items
globalData['game'] = data.game
globalData['findItem'] = data.findItem
globalData['run'] = run