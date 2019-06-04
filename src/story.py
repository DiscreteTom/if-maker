import re
from data import data
import msvcrt
from time import sleep

class story:
	@classmethod
	def printStory(cls, story_id):
		'''
		return False if story_id is not found in story file. story_id should be a number or a string
		'''
		f = open('.ifm/story', encoding='utf-8')
		# find the story
		while True:
			s = f.readline()
			if len(s) == 0:
				# EOF without finding out the story
				return False
			# use regex to find story token
			match = re.search('(\\{)\\s*(\\d+)(\\s*:\\s*([^ \\f\\n\\r\\t\\v\\}]+))?\\s*(\\})', s)
			if match:
				if story_id == match.group(4) or str(story_id) == match.group(2):
					# touch the story tag
					break
		# print the story
		skip = False
		while True:
			s = f.readline().strip()
			if len(s) == 0:
				# EOF or end of story
				return True
			cls.print(s, skip=skip)
			if not skip:
				if msvcrt.getwch() == '\u001B':
					# if `esc` is pressed
					skip = True

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