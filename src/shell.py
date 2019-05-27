from data import data

class shell:
	'''
	provide `shell.load`, `shell.unload` and `shell.parse`
	'''
	itemActions = {}

	@classmethod
	def load(cls, items):
		'''
		`items` can be a `str` or a `list`
		'''
		from translator import Translator
		# convert items to a list
		if isinstance(items, str):
			items = [items]

		for itemID in items:
			# judge existance
			if itemID not in data.items:
				continue
			if 'actions' not in data.items[itemID]:
				continue

			# add actions
			cls.itemActions[itemID] = data.items[itemID]['actions']

			if 'onLoad' in data.items[itemID]:
				translator.run(data.items[itemID]['onLoad'].replace('this["', 'data.items["' + itemID + '.'))

	@classmethod
	def unload(cls, items):
		'''
		`items` can be a `str` or a `list`
		'''
		from translator import translator
		# convert items to a list
		if isinstance(items, str):
			items = [items]

		for itemID in items:
			if itemID not in cls.itemActions:
				continue
			cls.itemActions.pop(itemID)
			if 'onUnload' in data.items[itemID]:
				translator.run(data.items[itemID]['onUnload'].replace('this["', 'data.items["' + itemID + '.'))
		return True

	@classmethod
	def parse(cls, cmd: str):
		from translator import translator
		cmd = cmd.split()
		# traverse actions
		for itemID in cls.itemActions:
			for action in cls.itemActions[itemID]:
				# try to match
				pattern = action['name'].split()
				# judge cmd length
				if len(cmd) != len(pattern):
					continue
				# match each part
				match = True
				params = {}
				for i in range(len(cmd)):
					if pattern[i] == 'this' and cmd[i] != data.items[itemID]['name']:
						# this
						match = False
						break
					elif pattern[i][0] == '(' and pattern[i][-1] == ')':
						# params
						params[pattern[1:-1]] = cmd[i]
					else:
						# normal
						if pattern[i] != cmd[i]:
							match = False
							break
				if match:
					return translator.run(action['code'].replace('this["', 'data.items["' + itemID + '.'))
		return False