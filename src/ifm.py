import os
import sys
import yaml
from refdict import refdict
import shutil
import re
import json
import xml.etree.ElementTree as ET

def processCode(code: str) -> str:
	index = code.rfind('^')
	if index == -1:
		return code
	else:
		return code[:index]

def mergeItemsAndClasses(items: dict, classes: dict, globalClasses: list):
	# traverse all items
	for key in items:
		item = items[key]
		if 'classes' not in item:
			item['classes'] = globalClasses
		else:
			for c in globalClasses:
				if c not in item['classes']:
					item['classes'].append(c)
		for classID in item['classes']:
			processSingleClass(classes, classID)
			merge(item, classes[classID])

def processSingleClass(classes: dict, classID: str):
	'''
	if `'classes' in classes[classID]`, merge those classes recursively
	'''
	if 'classes' not in classes[classID]:
		# not need to process
		return
	currentClass = classes[classID]
	# merge currentClass['classes'] to currentClass
	for classID in currentClass['classes']:
		# recursively process
		processSingleClass(classes, classID)
		targetClass = classes[classID]
		merge(currentClass, targetClass)
	currentClass.pop('classes')

def merge(higher: dict, lower: dict):
	'''
	merge those attributes below from lower to higher(higher will be changed):
	```
	result = {
		'name': '', # use higher's if higher's is not empty
		'description': '', # use higher's if higher's is not empty
		'actions': [ # merge, ignore conflict, lower's after higher's
			{
				'name': '',
				'code': ''
			}
		],
		'onLoad': '', # merge, ignore conflict, higher's after lower's
		'onUnload': '', # merge, ignore conflict, higher's after lower's
		'data': {} # merge, consider conflict, use higher's
	}
	```
	'''
	if len(higher['name']) == 0 and 'name' in lower:
		higher['name'] = lower['name']

	if len(higher['description']) == 0 and 'description' in lower:
		higher['description'] = lower['description']
	
	if 'actions' in lower:
		higher['actions'] += lower['actions']

	if 'onLoad' in lower:
		higher['onLoad'] = lower['onLoad'] + '\n' + higher['onLoad']

	if 'onUnload' in lower:
		higher['onUnload'] = lower['onUnload'] + '\n' + higher['onUnload']

	if 'data' in lower:
		for key in lower['data']:
			if key in higher['data'] and lower['data'][key] is not None:
				print('warning: data conflict, key=', key, ', using ', higher['data'][key], ' instead of ', lower['data'][key], sep='')
			else:
				higher['data'][key] = lower['data'][key]

def processIfdInclude(processType: str, modules: list):
	'''
	load files. missing attributes will be added. If file is empty or not exist, return empty dict

	`processType` should be one of `['items', 'classes']`
	'''
	# open root file
	try:
		f = open('_' + processType + '/index.ifd', encoding='utf-8')
		result = yaml.safe_load(f)
		f.close()
	except: 
		result = {}
	if result is None:
		result = {}
	# process root file include
	if 'include' in result:
		# include other file
		while len(result['include']):
			# load target file, order is not matter
			f = open('_' + processType + '/' + result['include'].pop(), encoding='utf-8')
			current = yaml.safe_load(f)
			f.close()
			# merge include
			if 'include' in current:
				result['include'] += current.pop('include')
			# merge other result
			for item in current:
				if item in result:
					merge(result[item], current[item])
				else:
					result[item] = current[item]
		# now result['include'] is empty
		result.pop('include')
	# process modules
	for module in modules:
		try:
			f = open('_modules/' + module + '/' + processType + '.ifd', encoding='utf-8')
			yml = yaml.safe_load(f)
			for item in yml:
				if item in result:
					merge(result[item], yml[item])
				else:
					result[item] = yml[item]
			f.close()
		except: pass
	# add missing attribute
	for itemID in result:
		if 'name' not in result[itemID]:
			result[itemID]['name'] = ''
		if 'description' not in result[itemID]:
			result[itemID]['description'] = ''
		if 'actions' not in result[itemID]:
			result[itemID]['actions'] = []
		if 'onLoad' not in result[itemID]:
			result[itemID]['onLoad'] = ''
		if 'onUnload' not in result[itemID]:
			result[itemID]['onUnload'] = ''
		if 'data' not in result[itemID]:
			result[itemID]['data'] = {}
	# process with `^`
	for itemID in result:
		result[itemID]['onLoad'] = processCode(result[itemID]['onLoad'])
		result[itemID]['onUnload'] = processCode(result[itemID]['onUnload'])
		for action in result[itemID]['actions']:
			action['code'] = processCode(action['code'])
	return result

def processStories():
	'''
	process _stories/index.ift, save result to .ifm/story
	- process `#include`
	- add xml header and root element
	'''
	fout = open('.ifm/story', 'w', encoding='utf-8')
	fout.write('<?xml version="1.0"?>')
	fout.write('<root>')
	storyQueue = ['index.ift']
	while len(storyQueue):
		fin = open('_stories/' + storyQueue.pop(), 'r', encoding='utf-8')
		while True:
			s = fin.readline()
			if len(s) == 0:
				# EOF
				break
			if s.startswith('#include '):
				# add another story file
				storyQueue.append(s.split()[1])
			else:
				# normal story
				fout.write(s)
		fin.close()
	fout.write('</root>')
	fout.close()
	# try to parse xml
	try:
		ET.parse('.ifm/story')
	except:
		print('wrong format story')
		errorHandler()

def itemsAddID(items: dict):
	for key in items:
		items[key]['id'] = key

def errorHandler():
	'''
	clear output folder and exit
	'''
	shutil.rmtree('.ifm')
	os._exit(1)

def getConfig() -> dict:
	'''
	generate .ifm/config and return config['make']
	'''
	f = open('_config.yml', encoding='utf-8')
	config = refdict(yaml.safe_load(f))
	f.close()

	configTemplate = {
		'project': {
			'name': config.get('project.name', 'untitled project'),
			'welcome': config.get('project.welcome', None)
		},
		'system': {
			'shell': {
				'prefix': config.get('system.shell.prefix', '>'),
				'exitCmd': config.get('system.shell.exitCmd', 'exit'),
				'errorMsg': config.get('system.shell.errorMsg', 'invalid command'),
				'history': config.get('system.shell.history', 10)
			},
			'print': {
				'interval': config.get('system.print.interval', 0.02),
				'indent': config.get('system.print.indent', ''),
				'skip': config.get('system.print.skip', False)
			},
		},
		'make': {
			'modules': config.get('make.modules', []),
			'globalClasses': config.get('make.globalClasses', []),
		},
		'mainMenu': config.get('mainMenu', ['start', 'exit']),
		'debug': config.get('debug', [])
	}

	result = configTemplate.pop('make')

	f = open('.ifm/config', 'w', encoding='utf-8')
	json.dump(configTemplate, f)
	f.close()
	return result

def new():
	'''
	`ifm new`: create a new project, create folders and files
	'''
	proName = 'untitled'
	if len(sys.argv) == 2:
		proName = input('please input the name of your project: (untitled)')
		if proName == '':
			proName = 'untitled'
	elif len(sys.argv) > 2:
		proName = sys.argv[2]
	
	os.mkdir('_classes')
	os.mkdir('_items')
	os.mkdir('_scripts')
	os.mkdir('_stories')
	open('_config.yml', 'w', encoding='utf-8').close()
	open('_classes/index.ifd', 'w', encoding='utf-8').close()
	open('_items/index.ifd', 'w', encoding='utf-8').close()
	open('_stories/index.ift', 'w', encoding='utf-8').close()
	# open('_scripts/index.yml', 'w', encoding='utf-8').close()

def make():
	'''
	`ifm make`: generate middle files to `.ifm/`, combine items and classes, ignore comments in stories, generate config
	'''
	try:
		os.mkdir('.ifm')
	except FileExistsError:
		pass
	config = getConfig()
	items = processIfdInclude('items', config['modules'])
	classes = processIfdInclude('classes', config['modules'])
	mergeItemsAndClasses(items, classes, config['globalClasses'])
	itemsAddID(items)
	f = open('.ifm/items', 'w', encoding='utf-8')
	json.dump(items, f)
	f.close()
	processStories()

if __name__ == '__main__':
	make()