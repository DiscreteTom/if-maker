import data

# itemActions = {
# 	'itemID': [
# 		{
# 			'name': [
# 				'type': str,
# 				'value': str
# 			],
# 			'code': str
# 		}
# 	]
# }
itemActions = {}

def mount(*items):
	'''
	mount `items` to shell so that shell can parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''
	import translator

	for itemID in items:
		if isinstance(itemID, list) or isinstance(itemID, tuple):
			# not a str, process list or tuple recursively
			if len(itemID):
				mount(*itemID)
			continue
		if isinstance(itemID, dict):
			mount(itemID['id'])
			continue
		# itemID is a str, judge `@`
		if itemID.startswith('@'):
			itemID = itemID[1:]
		# judge existance
		if itemID not in data.items:
			if 'debug.mount' in data.config:
				print('debug.mount:', itemID, 'not exist in items')
			continue
		if 'actions' not in data.items[itemID]:
			continue

		# add actions
		if 'debug.mount' in data.config:
			print('debug.mount: loading', itemID)
		itemActions[itemID] = data.items[itemID]['actions']

		if 'onMount' in data.items[itemID]:
			translator.run(data.items[itemID]['onMount'], {'this': data.items(itemID)})

def unmount(*items):
	'''
	unmount `items` from shell so that shell can not parse their commands

	`items` can be a list of:
	- `str` as item ID
	- `list` as a list of item ID
	- `tuple` as a list of item ID
	- `dict` as an existing item
	'''
	import translator

	for itemID in items:
		if isinstance(itemID, list) or isinstance(itemID, tuple):
			# not a str, process list or tuple recursively
			if len(itemID):
				unmount(*itemID)
			continue
		if isinstance(itemID, dict):
			unmount(itemID['id'])
			continue
		# itemID is a str, judge existance
		if itemID.startswith('@'):
			itemID = itemID[1:]
		if itemID not in itemActions:
			if 'debug.unmount' in data.config:
				print('debug.unmount:', itemID, 'not found in items')
			continue
		if 'debug.unmount' in data.config:
			print('debug.unmount: unloading', itemID)
		itemActions.pop(itemID)
		if 'onUnmount' in data.items[itemID]:
			translator.run(data.items[itemID]['onUnmount'], {'this': data.items(itemID)})
	return True

# TODO: add support for `[]`
def parse(cmd: str):
	'''
	parse a command
	'''
	if 'debug.parse' in data.config:
		print('debug.parse: parsing', cmd)
	# judge exit
	if cmd == data.config['system.shell.exitCmd']:
		import os
		os._exit(0)
	# normal parse
	import translator
	cmd = cmd.split()
	# traverse actions
	for itemID in itemActions:
		for action in itemActions[itemID]:
			# judge cmd length
			if len(cmd) != len(action['name']):
				continue
			# match each part
			match = True
			params = {}
			for i in range(len(cmd)):
				if action['name'][i]['type'] == 'THIS':
					if cmd[i] != data.items[itemID]['name']:
						# can not match `this`
						match = False
						break
				elif action['name'][i]['type'].startswith('OBJECT'):
					# match params
					className = ''
					if len(action['name'][i]['type'].split('.')) > 1:
						# class name exists
						className = action['name'][i]['type'].split('.')[1]
					targetID = data.findItem(cmd[i], className)
					if targetID:
						# target exists, assign id to params
						params[action['name'][i]['value']] = targetID
					else:
						match = False
						break
				elif action['name'][i]['type'] == 'ANY':
					params[action['name'][i]['value']] = cmd[i]
				else:
					# match literal text, action['name'][i]['type'] == 'LITERAL'
					if action['name'][i]['value'] != cmd[i]:
						match = False
						break
			if match:
				if 'debug.parse' in data.config:
					print('debug.parse: matching', action['name'], 'of', itemID)
				# process `this`
				params['this'] = data.items(itemID)
				return translator.run(action['code'], params)
	return False

def loadedItems() -> list:
	'''
	return a list of item id which are loaded in shell
	'''
	return itemActions.keys()

def actionWords():
	'''
	return a `set` of words appeared in itemActions.name
	'''
	result = set()
	for itemID in itemActions:
		for action in itemActions[itemID]:
			for word in action['name']:
				if word['type'] == 'LITERAL':
					result.add(word['value'])
	return result

def completer(text: str, state: int):
	# TODO: better completer
	# add items' name
	result = set([data.items[x]['name'] for x in loadedItems() if data.items[x]['name'].startswith(text)])
	# add data.completer
	result.update([x for x in data.completer if x.startswith(text)])
	# add words in actions
	result.update([x for x in actionWords() if x.startswith(text)])
	result = list(result) + [None]
	return result[state]