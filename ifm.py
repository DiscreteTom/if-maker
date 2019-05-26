import os
import sys
import yaml
from refdict import refdict
import shutil

def mergeItemsAndClasses(items: dict, classes: dict):
	# traverse all items
	for key in items:
		item = items[key]
		if 'classes' not in item:
			item['classes'] = ['object']
		for classID in item['classes']:
			item['classes'] = item['classes'] + ['object']
			processSingleClass(classes, classID)
			merge(item, classes[classID])

def processSingleClass(classes: dict, classID: str):
	if 'classes' not in classes[classID]:
		# not need to process
		return
	currentClass = classes[classID]
	# merge currentClass['classes'] to currentClass
	for classID in currentClass:
		# recursively process
		processSingleClass(classes, classID)
		targetClass = classes[classID]
		merge(currentClass, targetClass)
	currentClass.pop('classes')

def merge(higher: dict, lower: dict):
	'''
	merge those attributes below:
	```
	result = {
		'name': '', # use higher's
		'description': '', # use higher's
		'actions': [ # merge, ignore conflict, lower's after higher's
			{
				'name': '',
				'code': ''
			}
		],
		'onLoad': '', # merge, ignore conflict, higher's after lower's, separated by ';'
		'onUnload': '', # merge, ignore conflict, higher's after lower's, separated by ';'
		'data': {} # merge, consider conflict, use higher's
	}
	```
	'''
	if 'name' not in higher and 'name' in lower:
		higher['name'] = lower['name']
	if 'description' not in higher and 'description' in lower:
		higher['description'] = lower['description']
	if 'actions' in lower:
		if 'actions' in higher:
			higher['actions'] += lower['actions']
		else:
			higher['actions'] = lower['actions']
	if 'onLoad' in lower:
		if 'onLoad' in higher:
			higher['onLoad'] = lower['onLoad'] + ';' + higher['onLoad']
		else:
			higher['onLoad'] = lower['onLoad']
	if 'onUnload' in lower:
		if 'onUnload' in higher:
			higher['onUnload'] = lower['onUnload'] + ';' + higher['onUnload']
		else:
			higher['onUnload'] = lower['onUnload']
	if 'data' in lower:
		if 'data' not in higher:
			higher['data'] = lower['data']
		else:
			for key in lower['data']:
				if key in higher['data']:
					print('warning: data ignored: key =', key)
				else:
					higher[key] = lower[key]

def processYamlInclude(processType: str):
	'''
	`processType` should be one of `['items', 'classes']`
	'''
	# open root file
	f = open('_' + processType + '/index.yml', encoding='utf-8')
	result = yaml.safe_load(f)
	f.close()
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
			for key in current:
				if key not in result:
					result[key] = current[key]
				else:
					print(processType, 'conflict:', key)
					errorHandler()
		# now result['include'] is empty
		result.pop('include')
	return result

def errorHandler():
	'''
	clear output folder and exit
	'''
	shutil.rmtree('.ifm')
	os._exit(1)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('usage:\nifm [new|make]')
	if sys.argv[1] == 'new':
		proName = 'untitled'
		if len(sys.argv) == 2:
			proName = input('please input the name of your project: (untitled)')
			if proName == '':
				proName = 'untitled'
		elif len(sys.argv) > 2:
			proName = sys.argv[2]
		
		os.mkdir('_classes')
		os.mkdir('_result')
		os.mkdir('_scripts')
		os.mkdir('_stories')
		open('_config.yml', 'w', encoding='utf-8').close()
		open('_classes/index.yml', 'w', encoding='utf-8').close()
		open('_result/index.yml', 'w', encoding='utf-8').close()
		open('_stories/index.yml', 'w', encoding='utf-8').close()
		open('_scripts/index.yml', 'w', encoding='utf-8').close()
	elif sys.argv[1] == 'make':
		items = processYamlInclude('items')
		classes = processYamlInclude('classes')
		mergeItemsAndClasses(items, classes)
		os.mkdir('.ifm')
		f = open('.ifm/items', 'w+', encoding='utf-8')
		f.write(str(items))
		f.close()