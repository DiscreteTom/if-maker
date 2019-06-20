import re
from data import data
import msvcrt
from time import sleep
import xml.etree.ElementTree as ElementTree

class story:
	@classmethod
	def printStory(cls, story_id: str) -> bool:
		'''
		print the story whose id is `story_id`

		return False if story_id is not found in story file
		'''
		# find the story
		xml = ElementTree.parse('.ifm/story')
		stories = xml.findall('story')
		for story in stories:
			if story.get('id') == story_id:
				# print the story element
				cls.__printElement(story, data.config['system.print.skip'])
				return True
		return False

	@classmethod
	def __printElement(cls, el: ElementTree.Element, skip: bool) -> bool:
		'''
		print the text of `el` and parse its children, ignore the tag of `el`

		return `skip` if player pressed `esc`
		'''
		# print text
		if el.text:
			skip = cls.__printStoryText(el.text, skip)
		# parse each child and it's tail text
		for child in el:
			skip = cls.__parseElement(child, skip)
			# print tail text
			if child.tail:
				skip = cls.__printStoryText(child.tail, skip)
		return skip
	
	@classmethod
	def __printStoryText(cls, text: str, skip: bool) -> bool:
		'''
		`text` can contain `\\n`

		print `text` by lines, strip each line, skip empty lines, start with `config['system.print.indent']`

		return `skip`. `skip` will changed from `False` to `True` if player press `esc`
		'''
		for line in text.split('\n'):
			line = line.strip()
			if len(line):
				cls.print(line, skip = skip, indent = data.config['system.print.indent'])
				if not skip:
					if msvcrt.getwch() == '\u001B':
						# if `esc` is pressed
						skip = True
		return skip

	@classmethod
	def __parse(cls, cmd: str, value = '', params = {}):
		import translator
		print('cmd:', cmd)
		print('value:', value)
		print('params:', params)
		if cmd == 'code':
			translator.run(value, params)

	@classmethod
	def print(cls, *values: str, **kwargs):
		'''
		`print(values, ..., skip = True, sep = ' ', end = '\\n', indent = '')`

		print `values` as `str`, parse `{}` commands in `values`
		'''

		skip = True if 'skip' not in kwargs else kwargs['skip']
		sep = ' ' if 'sep' not in kwargs else kwargs['sep']
		end = '\n' if 'end' not in kwargs else kwargs['end']
		indent = '' if 'indent' not in kwargs else kwargs['indent']

		print(indent, end='')
		for i in range(len(values)):
			s = values[i]
			s = str(s)
			# test if this line is a command
			match = re.match("\\{\\s*([a-zA-Z][^ \\f\\n\\r\\t\\v:\\}]*)\\s*(:\\s*(([^}@'\"]+|('[^']*'|\"[^\"]*\")|\\s)+))?", s)
			if match:
				# this line is a command
				cmd = match.group(1)
				value = match.group(3).strip()
				params = {}
				while True:
					s = s[match.end():].strip()
					match = re.match("(@\\w+)\\s*=\\s*('[^']*'|\"[^\"]*\")", s)
					if not match:
						break
					params[match.group(1)[1:]] = match.group(2)[1:-1]
				cls.__parse(cmd, value, params)
				continue
			# this line is a story, parse value refs
			while True:
				match = re.search("(\\{\\{)(\\s*[^ \\f\\n\\r\\t\\v\\}]+\\s*)(\\}\\})", s)
				if not match:
					# no more value refs
					break
				s = s[:match.start()] + data.items[match.group(2).strip()] + s[match.end():]
			# print story
			if skip or 'system.printInterval' not in data.config or data.config['system.printInterval'] <= 0:
				# pring line by once
				print(s, end='', flush=True)
			else:
				# print line by char
				for c in s:
					print(c, end='', flush=True)
					sleep(data.config['system.printInterval'])
			print(sep, end='')
		print('', end=end)

	@classmethod
	def printItemList(cls, l: list, **kwargs):
		'''
		`l` should be a list of item id

		kwargs: `skip = True`, `indent = '- '`
		'''
		
		skip = True if 'skip' not in kwargs else kwargs['skip']
		indent = '- ' if 'indent' not in kwargs else kwargs['indent']

		for itemID in l:
			if itemID.startswith('@'):
				itemID = itemID[1:]
			cls.print(data.items[itemID]['name'], skip=skip, indent=indent)