from data import data

class Shell:
	'''
	provide `shell.load`, `shell.unload` and `shell.parse`
	'''
	itemActions = {}

	@classmethod
	def load(cls, itemID: str):
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

	@classmethod
	def unload(cls, itemID: str):
		'''
		remove actions of `itemID`, return False if `itemID` have not been loaded, otherwise return True
		'''
		if itemID not in cls.itemActions:
			return False
		cls.itemActions.pop(itemID)
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
					return Translator.do(action['code'])
		return False