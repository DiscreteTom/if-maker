from data import data

class shell:
	'''
	provide `shell.load`, `shell.unload` and `shell.parse`
	'''
	__itemActions = {}

	@classmethod
	def load(cls, *items):
		'''
		`items` can be a list of `str` or `list` or `tuple`
		'''
		import translator


		for itemID in items:
			if isinstance(itemID, list) or isinstance(itemID, tuple):
				# not a str, process list or tuple recursively
				cls.load(*itemID)
				continue
			# itemID is a str, judge existance
			if itemID not in data.items:
				continue
			if 'actions' not in data.items[itemID]:
				continue

			# add actions
			cls.__itemActions[itemID] = data.items[itemID]['actions']

			if 'onLoad' in data.items[itemID]:
				translator.run(data.items[itemID]['onLoad'].replace('this["', 'data.items["' + itemID + '.'))

	@classmethod
	def unload(cls, *items):
		'''
		`items` can be a list of `str` or `list` or `tuple`
		'''
		import translator
		# convert items to a list
		if isinstance(items, str):
			items = [items]

		for itemID in items:
			if isinstance(itemID, list) or isinstance(itemID, tuple):
				# not a str, process list or tuple recursively
				cls.unload(*itemID)
				continue
			# itemID is a str, judge existance
			if itemID not in cls.__itemActions:
				continue
			cls.__itemActions.pop(itemID)
			if 'onUnload' in data.items[itemID]:
				translator.run(data.items[itemID]['onUnload'].replace('this["', 'data.items["' + itemID + '.'))
		return True

	@classmethod
	def parse(cls, cmd: str):
		import translator
		cmd = cmd.split()
		# traverse actions
		for itemID in cls.__itemActions:
			for action in cls.__itemActions[itemID]:
				# try to match
				pattern = action['name'].split()
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
						params[pattern[i][1:-1]] = cmd[i]
					else:
						# normal
						if pattern[i] != cmd[i]:
							match = False
							break
				if match:
					# process `this`
					return translator.run(action['code'].replace('this["', 'data.items["' + itemID + '.'), params)
		return False