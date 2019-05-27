import re
from data import data
import msvcrt
from time import sleep

class story:
	@classmethod
	def tell(cls, story_id):
		'''
		return False if story_id is not found in story file. story_id should be a number or a string
		'''
		f = open('../.ifm/story', encoding='utf-8')
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
			if len(s) == 0 or s == '\n':
				# EOF or end of story
				return True
			cls.print(s, skip)
			if not skip:
				if msvcrt.getwch() == '\u001B':
					# if `esc` is pressed
					skip = True

	@classmethod
	def parse(cls, cmd: str, value = '', params = {}):
		print(cmd, value, params)

	@classmethod
	def print(cls, s: str, skip = False, end = '\n', indent = ''):
		'''
		print one line, parse commands and other things in `{}`
		'''
		# ignore comment
		s = s.split('#')[0].strip()
		if len(s) == 0:
			return
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
			cls.parse(cmd, value, params)
			return
		# this line is a story, parse value refs
		while True:
			match = re.search("(\\{\\{)(\\s*[^ \\f\\n\\r\\t\\v\\}]+\\s*)(\\}\\})", s)
			if not match:
				# no more value refs
				break
			s = s[:match.begin()] + data.items[match.group(2).strip()] + s[match.end():]
		# print story
		if skip or data.config['system.printInterval'] <= 0:
			# pring line by once
			print(indent, end='')
			print(s, end=end)
		else:
			# print line by char
			print(indent, end='')
			for c in s:
				print(c, end='', flush=True)
				sleep(data.config['system.printInterval'] / 1000)
			print('', end=end)