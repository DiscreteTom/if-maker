'''
use `data.config` to access config file, use `data.items` to access items file
'''

import yaml

class Data:
	config = {}
	items = {}
	def __init__(self):
		# load config
		f = open('_config.yml', encoding='utf-8')
		self.config = yaml.load(f)
		f.close()
		# load items
		f = open('_items.yml', encoding='utf-8')
		self.items = yaml.load(f)
		f.close()

data = Data()