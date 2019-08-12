import os
import sys
import yaml
from refdict import refdict
import shutil
import re
import json
import xml.etree.ElementTree as ET
import argparse

def removeInnerWhiteChars(s: str, left: str, right: str) -> str:
	'''
	remove all whitespaces and tab in `s` between all `left` and `right`
	'''
	startIndex = s.find(left)
	while startIndex != -1:
		endIndex = s.find(right, startIndex)
		if endIndex == -1:
			# no matching parentheses
			# TODO: print error msg
			errorHandler()
		s = s[:startIndex] + s[startIndex:endIndex].replace(' ', '').replace('\t', '') + s[endIndex:]
		# reset startIndex for next loop
		startIndex = s.find(left, s.find(right, startIndex))
	return s

def processActionName(data: dict) -> None:
	'''
	`data` should be `items` or `classes`

	change every action.name to this format:
	```
	name = [
		{
			'type': 'LITERAL',
			'value': 'value'
		}
	]
	```
	`type` can be `LITERAL`/`THIS`/`OBJECT.classname`/`ANY`
	'''
	for itemID in data:
		if 'actions' in data[itemID]:
			for action in data[itemID]['actions']:
				result = []
				action['name'] = removeInnerWhiteChars(action['name'], '(', ')')
				action['name'] = removeInnerWhiteChars(action['name'], '[', ']')
				result = action['name'].split()
				for i in range(len(result)):
					if result[i] == 'this':
						result[i] = {'type': 'THIS', 'value': 'this'}
					elif result[i].startswith('('):
						t = result[i][1:-1].split(':')
						result[i] = {'type': 'OBJECT', 'value': t[0]}
						if len(t) > 1:
							result[i]['type'] = result[i]['type'] + '.' + t[1] # format 'OBJECT.classname'
					elif result[i].startswith('['):
						result[i] = {'type': 'ANY', 'value': result[i][1:-1]}
					else:
						result[i] = {'type': 'LITERAL', 'value': result[i]}
				action['name'] = result

def processCode(code: str) -> str:
	'''
	remove chars after the last `^` of `code`(including `^`) and return
	'''
	index = code.rfind('^')
	if index == -1:
		return code
	else:
		return code[:index]

def processItemCode(items: dict):
	'''
	remove `^` from `onMount`/`onUnmount`/`action.code` of items
	'''
	for itemID in items:
		if 'onMount' in items[itemID]:
			items[itemID]['onMount'] = processCode(items[itemID]['onMount'])
		if 'onUnmount' in items[itemID]:
			items[itemID]['onUnmount'] = processCode(items[itemID]['onUnmount'])
		if 'actions' in items[itemID]:
			for action in items[itemID]['actions']:
				action['code'] = processCode(action['code'])

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

def mergeCode(lower: dict, higher: dict, key: str) -> None:
	'''
	`lower[key]` and `higher[key]` should be str
	
	`higher[key]` = `higher[key]` + '\\n' + `lower[key]`
	'''
	if key in higher:
		if key in lower:
			higher[key] += '\n' + lower[key]
	else:
		if key in lower:
			higher[key] = lower[key]


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
		'classes': [] # merge, remove duplicate value
	}
	```
	'''
	mergeValue(lower, higher, 'name')
	mergeValue(lower, higher, 'description')
	mergeList(lower, higher, 'actions')
	mergeList(lower, higher, 'classes')
	mergeCode(lower, higher, 'onMount')
	mergeCode(lower, higher, 'onUnmount')
	mergeDict(lower, higher, 'data')

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
	# process with `^`
	processItemCode(result)
	# process modules
	for module in modules:
		try:
			f = open('_modules/' + module + '/' + processType + '.ifd', encoding='utf-8')
			yml = yaml.safe_load(f)
			processItemCode(yml)
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
				# add other story files
				storyQueue += s.split()[1:]
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

def mergeValue(lower: dict, higher: dict, key: str) -> None:
	'''
	if `lower[key]` exists and `higher[key]` not exists, `higher[key] = lower[key]`
	'''
	if key in lower and key not in higher:
		higher[key] = lower[key]

def mergeList(lower: dict, higher: dict, key: str) -> None:
	'''
	if `higher[key]` and `lower[key]` exist, they should be list.
	
	merge list, ignore conflict, remove duplicate value
	'''
	# TODO: type test
	if key in lower:
		if key not in higher:
			higher[key] = []
		for value in lower[key]:
			if value not in higher[key]:
				higher[key].append(value)

def mergeDict(lower: dict, higher: dict, key: str) -> None:
	'''
	if `higher[key]` and `lower[key]` exist, they should be dict.

	merge dict, consider conflict, use higher's value if conflict
	'''
	# TODO: type test
	if key in lower:
		if key not in higher:
			higher[key] = {}
		for k in lower[key]:
			if k not in higher[key]:
				higher[key][k] = lower[key][k]

def mergeConfig(lower: dict, higher: dict) -> None:
	'''
	```
	result = {
		'project': {
			'name': # use higher's if higher's exists
		},
		'system': {
			'shell': {
				'prefix': # use higher's if higher's exists
				'exitCmd': # use higher's if higher's exists
				'errorMsg': # use higher's if higher's exists
			},
			'print': {
				'interval': # use higher's if higher's exist
				'indent': # use higher's if higher's exists
				'skip': # use higher's if higher's exists
			},
			'story': {
				'first': # use higher's if higher's exists
				'skip': # use higher's if higher's exists
			},
			'entry': # use higher's if higher's exists
		},
		'make': {
			'modules': # merge, ignore conflict
			'globalClasses': # merge, ignore conflict
		},
		'debug': # use higher's if higher's exists
		'data': # merge, consider conflict, use higher's
	}
	```
	'''
	mergeValue(lower, higher, 'project.name')
	mergeValue(lower, higher, 'system.shell.prefix')
	mergeValue(lower, higher, 'system.shell.exitCmd')
	mergeValue(lower, higher, 'system.shell.errorMsg')
	mergeValue(lower, higher, 'system.print.interval')
	mergeValue(lower, higher, 'system.print.indent')
	mergeValue(lower, higher, 'system.print.skip')
	mergeValue(lower, higher, 'system.story.first')
	mergeValue(lower, higher, 'system.story.skip')
	mergeValue(lower, higher, 'system.entry')
	mergeList(lower, higher, 'make.modules')
	mergeList(lower, higher, 'make.globalClasses')
	mergeList(lower, higher, 'debug')
	mergeDict(lower, higher, 'data')

def getConfig() -> dict:
	'''
	generate src/output/config and return config['make']
	'''
	# read original config
	f = open('_config.yml', encoding='utf-8')
	config = refdict(yaml.safe_load(f))
	f.close()

	# merge module config
	if 'make.modules' in config:
		i = 0
		while i < len(config['make.modules']):
			m = config['make.modules'][i]
			try:
				f = open('_modules/' + m + '/config.yml', 'r', encoding='utf-8')
				t = refdict(yaml.safe_load(f))
				mergeConfig(t, config)
				f.close()
			except:
				pass
			i += 1

	# add default value
	result = {
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
		'debug': config.get('debug', []),
		'data': config.get('data', None)
	}

	ret = result.pop('make')

	f = open('src/output/config', 'w', encoding='utf-8')
	json.dump(result, f)
	f.close()
	return ret

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

def processScripts(modules: list):
	'''
	combine scripts in _scripts into src/output/scripts.py
	'''
	fout = open('src/output/__init__.py', 'w', encoding='utf-8')
	# write header content
	f = open('src/output_header.py', 'r', encoding='utf-8')
	fout.write(f.read())
	f.close()
	# merge scripts in _scripts folder to output file
	for file in os.listdir('_scripts'):
		if file.endswith('.py') and file != 'ifmu.py':
			fin = open('_scripts/' + file, encoding='utf-8')
			fout.write(fin.read().replace('from ifmu import *', '') + '\n')
			fin.close()
	# merge scripts in modules to output file
	for module in modules:
		try:
			fin = open('_modules/' + module + '/scripts.py', 'r', encoding='utf-8')
			fout.write(fin.read().replace('from ifmu import *', '') + '\n')
			fin.close()
		except:
			pass
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
	processActionName(items)
	processActionName(classes)
	mergeItemsAndClasses(items, classes, config['globalClasses'])
	itemsAddID(items)
	f = open('src/output/items', 'w', encoding='utf-8')
	json.dump(items, f)
	f.close()
	processStories()
	processScripts(config['modules'])

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
newParser = subparsers.add_parser('new', help = 'Create a new project in current folder.')
newParser.add_argument('projectName', nargs='?', default='')
makeParser = subparsers.add_parser('make', help = 'Compile current project.')
runParser = subparsers.add_parser('run', help = 'Run current project.')
debugParser = subparsers.add_parser('debug', help = 'Compile and run current project.')
releaseParser = subparsers.add_parser('release', help = 'Package current project to an executable file.')
clearParser = subparsers.add_parser('clear', help = 'Clear current project.')
args = parser.parse_args()
if args.subparser == 'new':
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