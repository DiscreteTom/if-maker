from src.data import data
from src.translator import translator

class Shell:
	itemActions = {}

	def load(self, itemID: str):
		# judge existance
		if itemID not in data.items:
			return False
		if 'actions' not in data.items[itemID]:
			return False

		# clear actions about this item
		self.itemActions[itemID] = []

		# add actions
		for action in data.items[itemID]['actions']:
			action['name'] = action['name'].split()
			self.itemActions[itemID].append(action)

	def unload(self, itemID: str):
		'''
		remove actions of `itemID`, return False if `itemID` have not been loaded, otherwise return True
		'''
		if itemID not in self.itemActions:
			return False
		self.itemActions.pop(itemID)
		return True

	def parse(self, cmd: str):
		cmd = cmd.split()
		# traverse actions
		for itemID in self.itemActions.keys:
			for action in self.itemActions[itemID]:
				# change 'this' in action.name to item.name
				for i in len(action['name']):
					if action['name'][i] == 'this':
						action['name'][i] = data.items[itemID]['name']
				if action['name'] == cmd:
					return translator.do(action['code'])
		return False

shell = Shell()