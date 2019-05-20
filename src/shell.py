from data import data

class Shell:
	'''
	provide `shell.load`, `shell.unload` and `shell.parse`
	'''
	itemActions = {}

	@classmethod
	def load(cls, *items: str):
		from translator import Translator
		for itemID in items:
			# judge existance
			if itemID not in data.items:
				return False
			if 'actions' not in data.items[itemID]:
				return False

			# clear actions about this item
			cls.itemActions[itemID] = []

			# add actions
			for action in data.items[itemID]['actions']:
				action['name'] = action['name'].split()
				cls.itemActions[itemID].append(action)

			if 'onLoad' in data.items[itemID]:
				Translator.do(data.items[itemID]['onLoad'].replace('this', 'data.items["' + itemID + '"]'))

	@classmethod
	def unload(cls, *items: str):
		'''
		remove actions of `itemID`, return False if `itemID` have not been loaded, otherwise return True
		'''
		for itemID in items:
			if itemID not in cls.itemActions:
				return False
			cls.itemActions.pop(itemID)
			if 'onUnload' in data.items[itemID]:
				Translator.do(data.items[itemID]['onUnload'].replace('this', 'data.items["' + itemID + '"]'))
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
					return Translator.do(action['code'].replace('this', 'data.items["' + itemID + '"]'))
		return False