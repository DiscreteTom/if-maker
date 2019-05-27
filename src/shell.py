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

			# if 'onLoad' in data.items[itemID]:
				# translator.run(data.items[itemID]['onLoad'].replace('this', 'data.items["' + itemID + '"]'))

	@classmethod
	def unload(cls, items):
		'''
		`items` can be a `str` or a `list`
		'''
		# convert items to a list
		if isinstance(items, str):
			items = [items]

		for itemID in items:
			if itemID not in cls.itemActions:
				continue
			cls.itemActions.pop(itemID)
			# if 'onUnload' in data.items[itemID]:
				# translator.run(data.items[itemID]['onUnload'].replace('this', 'data.items["' + itemID + '"]'))
		return True

	@classmethod
	def parse(cls, cmd: str):
		'''
		if `cmd` is valid, return the return value of action's code. if `cmd` is invalid, return False.
		if you want to stop parse, return 'stop-shell'
		'''
		from translator import Translator
		cmd = cmd.split()
		# traverse actions
		for itemID in cls.itemActions.keys():
			for action in cls.itemActions[itemID]:
				# change 'this' in action.name to item.name
				for i in range(len(action['name'])):
					if action['name'][i] == 'this':
						action['name'][i] = data.items[itemID]['name']
				if action['name'] == cmd:
					return translator.run(action['code'].replace('this', 'data.items["' + itemID + '"]'))
		return False