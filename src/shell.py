from data import data

class shell:
	'''
	provide `shell.mount`, `shell.unmount` and `shell.parse`
	'''

	# itemActions = {
	# 	'itemID': [
	# 		{
	# 			'name': str[],
	# 			'code': str
	# 		}
	# 	]
	# }
	__itemActions = {}

	@classmethod
	def mount(cls, *items):
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
					cls.mount(*itemID)
				continue
			if isinstance(itemID, dict):
				cls.mount(itemID['id'])
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
			cls.__itemActions[itemID] = []
			for action in data.items[itemID]['actions']:
				cls.__itemActions[itemID].append({'name': action['name'].split(), 'code': action['code']})

			if 'onMount' in data.items[itemID]:
				translator.run(data.items[itemID]['onMount'], {'this': data.items(itemID)})

	@classmethod
	def unmount(cls, *items):
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
					cls.unmount(*itemID)
				continue
			if isinstance(itemID, dict):
				cls.unmount(itemID['id'])
				continue
			# itemID is a str, judge existance
			if itemID.startswith('@'):
				itemID = itemID[1:]
			if itemID not in cls.__itemActions:
				if 'debug.unmount' in data.config:
					print('debug.unmount:', itemID, 'not found in items')
				continue
			if 'debug.unmount' in data.config:
				print('debug.unmount: unloading', itemID)
			cls.__itemActions.pop(itemID)
			if 'onUnmount' in data.items[itemID]:
				translator.run(data.items[itemID]['onUnmount'], {'this': data.items(itemID)})
		return True

	@classmethod
	def parse(cls, cmd: str):
		if 'debug.parse' in data.config:
			print('debug.parse: parsing', cmd)
		import translator
		cmd = cmd.split()
		# traverse actions
		for itemID in cls.__itemActions:
			for action in cls.__itemActions[itemID]:
				# try to match
				pattern = action['name']
				# judge cmd length
				if len(cmd) != len(pattern):
					continue
				# match each part
				match = True
				params = {}
				for i in range(len(cmd)):
					if pattern[i] == 'this':
						if cmd[i] != data.items[itemID]['name']:
							# can not match `this`
							match = False
							break
					elif pattern[i][0] == '(' and pattern[i][-1] == ')':
						# match params
						targetID = data.findItem(cmd[i])
						if targetID:
							# target exist, get id
							params[pattern[i][1:-1]] = targetID
						else:
							break
					else:
						# normal
						if pattern[i] != cmd[i]:
							match = False
							break
				if match:
					# process `this`
					if 'debug.parse' in data.config:
						print('debug.parse: matching', action['name'], 'of', itemID)
					params['this'] = data.items(itemID)
					return translator.run(action['code'], params)
		return False

	@classmethod
	def loadedItems(cls) -> list:
		'''
		return a list of item id which are loaded in shell
		'''
		return cls.__itemActions.keys()

	@classmethod
	def data(cls) -> dict:
		return cls.__itemActions

	@classmethod
	def load(cls, data = {}):
		cls.__itemActions = data

	@classmethod
	def actionWords(cls):
		'''
		return a `set` of words appeared in itemActions.name
		'''
		result = set()
		for itemID in cls.__itemActions:
			for action in cls.__itemActions[itemID]:
				for word in action['name']:
					if not word.startswith('('):
						result.add(word)
		return result

def completer(text: str, state: int):
	result = set([data.items[x]['name'] for x in shell.loadedItems() if data.items[x]['name'].startswith(text)])
	result.update([x for x in data.completer if x.startswith(text)])
	result.update([x for x in shell.actionWords() if x.startswith(text)])
	result = list(result) + [None]
	return result[state]