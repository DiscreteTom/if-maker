'''
- `data.config` to access config variables
- `data.items` to access items
- `data.game` to access global variables
- `data.completer` to add user defined words
- `data.findItem(itemName)` to get item id
'''

from refdict import refdict
import json

class Data:
	def __init__(self):
		# load config
		f = open('.ifm/config', encoding='utf-8')
		self.config = refdict(json.load(f))
		f.close()
		# load items
		f = open('.ifm/items', encoding='utf-8')
		self.items = refdict(json.load(f))
		f.close()
		# user defined global data
		self.game = refdict({})
		self.completer = []
	def findItem(self, itemName: str):
		'''
		return itemID
		'''
		for itemID in self.items:
			if self.items[itemID]["name"] == itemName:
				return itemID
		return None

data = Data()