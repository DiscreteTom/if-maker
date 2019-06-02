from data import data

class shell:
	'''
	provide `shell.load`, `shell.unload` and `shell.parse`
	'''
	__itemActions = {}

	@classmethod
	def load(cls, *items):
		'''
		`items` can be a list of `str` or `list` or `tuple` or `dict`
		'''
		import translator

		for itemID in items:
			if isinstance(itemID, list) or isinstance(itemID, tuple):
				# not a str, process list or tuple recursively
				if len(itemID):
					cls.load(*itemID)
				continue
			if isinstance(itemID, dict):
				cls.load(itemID['id'])
				continue
			# itemID is a str, judge `@`
			if itemID.startswith('@'):
				itemID = itemID[1:]
			# judge existance
			if itemID not in data.items:
				if 'debug.load' in data.config:
					print('debug.load:', itemID, 'not exist in items')
				continue
			if 'actions' not in data.items[itemID]:
				continue

			# add actions
			if 'debug.load' in data.config:
				print('debug.load: loading', itemID)
			cls.__itemActions[itemID] = []
			for action in data.items[itemID]['actions']:
				cls.__itemActions[itemID].append({'name': action['name'].split(), 'code': action['code']})

			if 'onLoad' in data.items[itemID]:
				translator.run(data.items[itemID]['onLoad'], {'this': data.items(itemID)})

	@classmethod
	def unload(cls, *items):
		'''
		`items` can be a list of `str` or `list` or `tuple` or `dict`
		'''
		import translator

		for itemID in items:
			if isinstance(itemID, list) or isinstance(itemID, tuple):
				# not a str, process list or tuple recursively
				if len(itemID):
					cls.unload(*itemID)
				continue
			if isinstance(itemID, dict):
				cls.unload(itemID['id'])
				continue
			# itemID is a str, judge existance
			if itemID.startswith('@'):
				itemID = itemID[1:]
			if itemID not in cls.__itemActions:
				if 'debug.unload' in data.config:
					print('debug.unload:', itemID, 'not found in items')
				continue
			if 'debug.unload' in data.config:
				print('debug.unload: unloading', itemID)
			cls.__itemActions.pop(itemID)
			if 'onUnload' in data.items[itemID]:
				translator.run(data.items[itemID]['onUnload'], {'this': data.items(itemID)})
		return True

	@classmethod
	def getComletion(cls, pos: int, part: str):
		'''
		return the rest of a command

		`pos` start from 1
		'''
		if not len(part):
			return ''
		for itemID in cls.__itemActions:
			for action in cls.__itemActions[itemID]:
				if len(action['name']) < pos:
					continue
				current = action['name'][pos - 1]
				if current[0] == '(':
					# it's a param
					continue
				if current == 'this':
					current = data.items[itemID]['name']
				if current.startswith(part):
					return current[len(part):]
		return ''


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