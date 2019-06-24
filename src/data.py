'''
- `data.config` to access config variables
- `data.items` to access items
- `data.game` to access global variables
- `data.completer` to add user defined words
- `data.findItem(itemName)` to get item id
- `data.save/load(fileName)` to save/mount game progress
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
	
	def save(self, fileName: str):
		'''
		save game progress to `fileName`
		'''
		f = open(fileName, 'w', encoding='utf-8')
		result = {
			'items': str(self.items),
			'config': str(self.config),
			'game': str(self.game)
		}
		json.dump(result, f)
		f.close()
	
	def load(self, fileName: str):
		'''
		load game progress from `fileName`
		'''
		try:
			f = open(fileName, encoding='utf-8')
			d = json.load(f)
			self.completer = eval(d.completer)
			self.items = eval(d.items)
			self.config = eval(d.config)
			self.game = eval(d.game)
			f.close()
		except:
			print('can not load SAVE file')

data = Data()