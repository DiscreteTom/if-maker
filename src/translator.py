def run(code: str, params = {}):
	from shell import shell
	from data import data
	from story import story
	if 'debug.run' in data.config:
		print('debug.run: running', code, 'params:', params)
	result = None
	# construct env
	params['load'] = shell.load
	params['unload'] = shell.unload
	params['parse'] = shell.parse
	params['print'] = story.print
	params['printStory'] = story.printStory
	params['printItemList'] = story.printItemList
	params['config'] = data.config
	params['items'] = data.items
	params['game'] = data.game
	params['findItem'] = data.findItem
	params['run'] = run
	result = exec(code, {}, params)
	return result
