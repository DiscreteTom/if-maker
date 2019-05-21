'''
use `data.config` to access config file, use `data.items` to access items file
'''

import yaml

class Data:
	def __init__(self):
		# load config
		f = open('../_config.yml', encoding='utf-8')
		self.config = yaml.safe_load(f)
		f.close()
		# load items
		f = open('../_items.yml', encoding='utf-8')
		self.items = yaml.safe_load(f)
		f.close()
		# user defined global data
		self.globalData = {}
	def findItem(self, itemName: str):
		'''
		return itemID
		'''
		for itemID in self.items:
			if items[itemID]["name"] == itemName:
				return itemID
		return None

data = Data()