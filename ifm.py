import os
import sys
import yaml
from refdict import refdict
import shutil
import re
import json
import xml.etree.ElementTree as ET
import urllib.request
import argparse

def processCode(code: str) -> str:
	'''
	remove chars after the last `^` of `code`(including `^`) and return
	'''
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
		'onMount': '', # merge, ignore conflict, higher's after lower's
		'onUnmount': '', # merge, ignore conflict, higher's after lower's
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

	if 'onMount' in lower:
		higher['onMount'] = lower['onMount'] + '\n' + higher['onMount']

	if 'onUnmount' in lower:
		higher['onUnmount'] = lower['onUnmount'] + '\n' + higher['onUnmount']

	if 'data' in lower:
		for key in lower['data']:
			if key in higher['data'] and lower['data'][key] is not None:
				print('warning: data conflict, key=', key, ', using ', higher['data'][key], ' instead of ', lower['data'][key], sep='')
			else:
				higher['data'][key] = lower['data'][key]

def processIfdInclude(processType: str, modules: list):
	'''
	load files, missing attributes will be added. If file is empty or not exist, return empty dict

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
		if 'onMount' not in result[itemID]:
			result[itemID]['onMount'] = ''
		if 'onUnmount' not in result[itemID]:
			result[itemID]['onUnmount'] = ''
		if 'data' not in result[itemID]:
			result[itemID]['data'] = {}
	# process with `^`
	for itemID in result:
		result[itemID]['onMount'] = processCode(result[itemID]['onMount'])
		result[itemID]['onUnmount'] = processCode(result[itemID]['onUnmount'])
		for action in result[itemID]['actions']:
			action['code'] = processCode(action['code'])
	return result

def processStories():
	'''
	process _stories/index.ift, save result to src/output/story
	- process `#include`
	- add xml header and root element
	'''
	fout = open('src/output/story', 'w', encoding='utf-8')
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
		ET.parse('src/output/story')
	except:
		print('wrong format story')
		errorHandler()

def itemsAddID(items: dict):
	for key in items:
		items[key]['id'] = key

def errorHandler():
	'''
	clear src/output folder and exit
	'''
	shutil.rmtree('src/output')
	os._exit(1)

def getConfig() -> dict:
	'''
	generate src/output/config and return config['make']
	'''
	f = open('_config.yml', encoding='utf-8')
	config = refdict(yaml.safe_load(f))
	f.close()

	configTemplate = {
		'project': {
			'name': config.get('project.name', 'untitled project'),
		},
		'system': {
			'shell': {
				'prefix': config.get('system.shell.prefix', '>'),
				'exitCmd': config.get('system.shell.exitCmd', 'exit'),
				'errorMsg': config.get('system.shell.errorMsg', 'invalid command'),
			},
			'print': {
				'interval': config.get('system.print.interval', 0.02),
				'indent': config.get('system.print.indent', ''),
				'skip': config.get('system.print.skip', True)
			},
			'story': {
				'first': config.get('system.story.first', '0'),
				'skip': config.get('system.story.skip', False)
			},
			'entry': config.get('system.entry', 'ifmain')
		},
		'make': {
			'modules': config.get('make.modules', []),
			'globalClasses': config.get('make.globalClasses', []),
		},
		'debug': [] if config.get('debug', []) is None else config.get('debug', []),
		'data': config.get('data', None)
	}

	result = configTemplate.pop('make')

	f = open('src/output/config', 'w', encoding='utf-8')
	json.dump(configTemplate, f)
	f.close()
	return result

def new(proName = ''):
	'''
	`ifm new`: create a new project, create folders and files
	'''
	if len(proName) == 0:
		proName = input('please input the name of your project: (untitled)')
	if len(proName) == 0:
		proName = 'untitled'
	# TODO: add more error handling codes below
	try:
		os.mkdir('_classes')
		os.mkdir('_items')
		os.mkdir('_scripts')
		os.mkdir('_modules')
		os.mkdir('_stories')
		f = open('_config.yml', 'w', encoding='utf-8')
		f.write('project:\n  name: "' + proName + '"')
		f.close()
		f = open('_items/index.ifd', 'w', encoding='utf-8')
		f.close()
		f = open('_classes/index.ifd', 'w', encoding='utf-8')
		f.close()
		f = open('_stories/index.ift', 'w', encoding='utf-8')
		f.close()
		f = open('_scripts/main.py', 'w', encoding='utf-8')
		f.write("from ifmu import *\n\ndef ifmain():\n	printf('Hello World!')")
		f.close()
		f = open('_scripts/ifmu.py', 'w', encoding='utf-8')
		f2 = open('src/ifmu.py', encoding='utf-8')
		f.write(f2.read())
		f2.close()
		f.close()
	except:
		print('create project failed.\ntry "ifm clear" first.')

def processScripts():
	'''
	combine scripts in _scripts into src/output/scripts.py
	'''
	fout = open('src/output/__init__.py', 'w', encoding='utf-8')
	f = open('src/output_header.py', 'r', encoding='utf-8')
	fout.write(f.read())
	f.close()
	for file in os.listdir('_scripts'):
		if file.endswith('.py') and file != 'ifmu.py':
			fin = open('_scripts/' + file, encoding='utf-8')
			fout.write(fin.read().replace('from ifmu import *', '') + '\n')
			fin.close()
	fout.close()

def make():
	'''
	`ifm make`: generate middle files to `src/output/`, combine items with classes, process stories to xml, generate config
	'''
	try:
		os.mkdir('src/output')
	except FileExistsError:
		pass
	config = getConfig()
	items = processIfdInclude('items', config['modules'])
	classes = processIfdInclude('classes', config['modules'])
	mergeItemsAndClasses(items, classes, config['globalClasses'])
	itemsAddID(items)
	f = open('src/output/items', 'w', encoding='utf-8')
	json.dump(items, f)
	f.close()
	processStories()
	processScripts()

def clear():
	import shutil
	try:
		shutil.rmtree('_scripts')
	except:
		pass
	try:
		shutil.rmtree('_items')
	except:
		pass
	try:
		shutil.rmtree('_stories')
	except:
		pass
	try:
		shutil.rmtree('_classes')
	except:
		pass
	try:
		shutil.rmtree('_modules')
	except:
		pass
	try:
		shutil.rmtree('src/output')
	except:
		pass
	try:
		os.remove('_config.yml')
	except:
		pass

def run():
	sys.path.append(os.getcwd() + '/src')
	os.chdir('src')
	import controller
	controller.start()

# construct parser
parser = argparse.ArgumentParser('ifm')
subparsers = parser.add_subparsers(dest='subparser')
installParser = subparsers.add_parser('install', help = 'Install if-maker in current folder. Network access is needed.')
newParser = subparsers.add_parser('new', help = 'Create a new project in current folder.')
newParser.add_argument('projectName', nargs='?', default='')
makeParser = subparsers.add_parser('make', help = 'Compile current project.')
runParser = subparsers.add_parser('run', help = 'Run current project.')
debugParser = subparsers.add_parser('debug', help = 'Compile and run current project.')
releaseParser = subparsers.add_parser('release', help = 'Package current project to an executable file.')
clearParser = subparsers.add_parser('clear', help = 'Clear current project.')
args = parser.parse_args()
if args.subparser == 'install':
	# TODO: add error handling
	# TODO: add progress bar
	os.mkdir('src')
	open('src/controller.py', 'w', encoding='utf-8').close()
	open('src/data.py', 'w', encoding='utf-8').close()
	open('src/ifmu.py', 'w', encoding='utf-8').close()
	open('src/output_header.py', 'w', encoding='utf-8').close()
	open('src/shell.py', 'w', encoding='utf-8').close()
	open('src/story.py', 'w', encoding='utf-8').close()
	open('src/translator.py', 'w', encoding='utf-8').close()
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/controller.py', 'src/controller.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/data.py', 'src/data.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/data.py', 'src/ifmu.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/data.py', 'src/output_header.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/shell.py', 'src/shell.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/story.py', 'src/story.py')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/DiscreteTom/if-maker/master/src/translator.py', 'src/translator.py')
elif args.subparser == 'new':
	new(args.projectName)
elif args.subparser == 'make':
	make()
elif args.subparser == 'run':
	run()
elif args.subparser == 'debug':
	make()
	run()
elif args.subparser == 'package':
	# TODO
	pass
elif args.subparser == 'clear':
	clear()