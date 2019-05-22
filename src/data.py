'''
use `data.config` to access config file, use `data.items` to access items file
'''

from refdict import refdict
import yaml

class Data:
	def __init__(self):
		# load config
		f = open('../_config.yml', encoding='utf-8')
		self.config = refdict(yaml.safe_load(f))
		f.close()
		# load items
		f = open('../_items.yml', encoding='utf-8')
		self.items = refdict(yaml.safe_load(f))
		f.close()
		# user defined global data
		self.globalData = refdict({})
	def findItem(self, itemName: str):
		'''
		return itemID
		'''
		for itemID in self.items:
			if items[itemID]["name"] == itemName:
				return itemID
		return None

data = Data()