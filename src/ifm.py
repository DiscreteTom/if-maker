import os
import sys
import yaml
from refdict import refdict
import shutil

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
		open('_config.yml', 'w').close()
		open('_classes/index.yml', 'w').close()
		open('_result/index.yml', 'w').close()
		open('_stories/index.yml', 'w').close()
		open('_scripts/index.yml', 'w').close()
	elif sys.argv[1] == 'make':
		items = processYamlInclude('items')
		classes = processYamlInclude('classes')

def mergeItemsAndClasses(items: dict, classes: dict):
	pass

def processClasses(classses: dict):
	pass

def processYamlInclude(processType: str):
	'''
	`processType` should be one of `['items', 'classes']`

	write result to .ifm/items and .ifm/classes
	'''
	# open root file
	f = open('_' + processType + '/index.yml')
	result = yaml.safe_load(f)
	f.close()
	if 'include' in result:
		# include other file
		while len(result['include']):
			# load target file, order is not matter
			f = open('_' + processType + '/' + result['include'].pop())
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