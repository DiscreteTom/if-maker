import os
import sys
import yaml
from refdict import refdict
import shutil
import re
import json

def mergeItemsAndClasses(items: dict, classes: dict, globalClasses: list):
	if items is None:
		return
	if classes is None:
		return
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
	load files. missing attributes will be added

	`processType` should be one of `['items', 'classes']`
	'''
	# open root file
	f = open('_' + processType + '/index.ifd', encoding='utf-8')
	result = yaml.safe_load(f)
	f.close()
	if result is None:
		return None
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
	for item in result:
		if 'name' not in result[item]:
			result[item]['name'] = ''
		if 'description' not in result[item]:
			result[item]['description'] = ''
		if 'actions' not in result[item]:
			result[item]['actions'] = []
		if 'onLoad' not in result[item]:
			result[item]['onLoad'] = ''
		if 'onUnload' not in result[item]:
			result[item]['onUnload'] = ''
		if 'data' not in result[item]:
			result[item]['data'] = {}
	return result

def processStories():
	'''
	process _stories/index.ift, save result to .ifm/story
	- get rid of comments
	- process `#include`
	- process `##` as `#`
	'''
	fout = open('.ifm/story', 'w', encoding='utf-8')
	storyQueue = ['index.ift']
	while len(storyQueue):
		fin = open('_stories/' + storyQueue.pop(), 'r', encoding='utf-8')
		while True:
			s = fin.readline()
			if len(s) == 0:
				# EOF
				break
			s = s.strip() + '\n'
			if s.startswith('#include '):
				# add another story file
				storyQueue.append(s.split()[1])
			else:
				# normal story, get rid of comment
				match = re.search("#[^#]", s)
				if match:
					# comment exist, remove comment
					s = s[0:match.start()] + '\n'
					if len(s) == 1:
						# this line has nothing but comment, do not output
						continue
				fout.write(s.replace('##', '#'))
		fin.close()
	fout.close()

def itemsAddID(items: dict):
	if items is None:
		return
	for key in items:
		items[key]['id'] = key

def processItemsCode(items: dict):
	'''
	get rid of `^`
	'''
	if items is None:
		return
	for key in items:
		items[key]['onLoad'] = items[key]['onLoad'].replace('^\n', '')
		items[key]['onUnload'] = items[key]['onUnload'].replace('^\n', '')
		for action in items[key]['actions']:
			action['code'] = action['code'].replace('^\n', '')

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
			'name': 'untitled project' if 'project.name' not in config else config['project.name'],
			'welcome': '' if 'project.welcome' not in config else config['project.welcome']
		},
		'system': {
			'shell': {
				'prefix': '>' if 'system.shell.prefix' not in config else config['system.shell.prefix'],
				'exitCmd': 'exit' if 'system.shell.exitCmd' not in config else config['system.shell.exitCmd'],
				'errorMsg': 'invalid command' if 'system.shell.errorMsg' not in config else config['system.shell.errorMsg']
			},
			'printInterval': 0.02 if 'system.printInterval' not in config else config['system.printInterval'],
			'history': 10 if 'system.history' not in config else config['system.history']
		},
		'make': {
			'globalClasses': [] if 'make.globalClasses' not in config else config['make.globalClasses'],
			'modules': [] if 'make.modules' not in config else config['make.modules']
		},
		'mainMenu': ['start', 'exit'] if 'mainMenu' not in config else config['mainMenu'],
		'debug': [] if 'debug' not in config or not isinstance(config['debug'], list) else config['debug']
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
	processItemsCode(items)
	f = open('.ifm/items', 'w', encoding='utf-8')
	json.dump(items, f)
	f.close()
	processStories()