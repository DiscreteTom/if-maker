import re
import data
import msvcrt
from time import sleep
import xml.etree.ElementTree as ElementTree

def print(*values: str, **kwargs):
	'''
	`print(values, ..., skip = config['system.print.skip'], sep = ' ', end = '\\n', indent = config['system.print.indent'])`

	replace variables in `{{}}` with its value
	'''
	skip = kwargs.get('skip', data.config['system.print.skip'])
	sep = kwargs.get('sep', ' ')
	end = kwargs.get('end', '\n')
	indent = kwargs.get('indent', data.config['system.print.indent'])

	print(indent, end='')
	for i in range(len(values)):
		value = values[i]
		s = str(value)
		# this line is a story, parse value refs
		while True:
			match = re.search("(\\{\\{)(\\s*[^ \\f\\n\\r\\t\\v\\}]+\\s*)(\\}\\})", s)
			if not match:
				# no more value refs
				break
			from translator import globalData
			s = s[:match.start()] + eval(match.group(2).strip(), globalData) + s[match.end():]
		# print story
		if skip or 'system.print.interval' not in data.config or data.config['system.print.interval'] <= 0:
			# pring line by once
			print(s, end='', flush=True)
		else:
			# print line by char
			for c in s:
				print(c, end='', flush=True)
				sleep(data.config['system.print.interval'])
		if i != len(values) - 1:
			print(sep, end='')
	print('', end=end)

def printStory(story_id: str) -> bool:
	'''
	print the story whose id is `story_id`

	return False if story_id is not found in story file
	'''
	# find the story
	xml = ElementTree.parse('output/story')
	stories = xml.findall('story')
	for story in stories:
		if story.get('id') == story_id:
			# print the story element
			__printElement(story, data.config['system.story.skip'])
			return True
	return False

def __printElement(el: ElementTree.Element, skip: bool) -> bool:
	'''
	print the text of `el` and parse its children, ignore the tag of `el`

	return `skip` if player pressed `esc`
	'''
	# print text
	if el.text:
		skip = __printStoryText(el.text, skip)
	# parse each child and it's tail text
	for child in el:
		skip = __parseElement(child, skip)
		# print tail text
		if child.tail:
			skip = __printStoryText(child.tail, skip)
	return skip

def __printStoryText(text: str, skip: bool) -> bool:
	'''
	`text` can contain `\\n`

	print `text` by lines, strip each line, skip empty lines, start with `config['system.print.indent']`

	return `skip`. `skip` will changed from `False` to `True` if player press `esc`
	'''
	for line in text.split('\n'):
		line = line.strip()
		if len(line):
			print(line, skip = skip, indent = data.config['system.print.indent'])
			if not skip:
				if msvcrt.getwch() == '\u001B':
					# if `esc` is pressed
					skip = True
	return skip

def __parseElement(el: ElementTree.Element, skip: bool) -> bool:
	'''
	parse `el` according to its tag, return `skip`
	'''
	localData = {}
	if el.tag == 'if':
		if eval(el.get('condition')):
			__printElement(el)
	elif el.tag == 'while':
		while eval(el.get('condition')):
			__printElement(el)
	elif el.tag == 'input':
		if el.get('prompt'):
			print(el.get('prompt'), skip = skip, end = '')
			localData[el.text] = input()
	elif el.tag == 'code':
		from translator import run
		run(el.text, localData)

def printItemList(l: list, skip = True, indent = '- ', sep = '\n', end = '\n'):
	'''
	`l` should be a list of item id, print those names
	'''
	for i in range(len(l)):
		itemID = l[i]
		if itemID.startswith('@'):
			itemID = itemID[1:]
		print(data.items[itemID]['name'], skip=skip, indent=indent, end='')
		if i != len(l) - 1:
			print(sep, skip = skip, end = '')
	print(end, skip=skip, end='')