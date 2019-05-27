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
	def parse(cls, s: str):
		'''
		parse command in story, format: `{operation: value @params="params value"}`
		'''
		from translator import translator
		match = re.search('\\{([^}:]+)\\s*(:\\s*([^}]+))?\\}', s)
		op = match.group(1)
		value = match.group(3)
		if op == 'bgm':
			pass
		elif op == 'call':
			pass
		elif op == 'code':
			translator.run(value)

	@classmethod
	def print(cls, s: str, skip = False, end = '\n', indent = ''):
		'''
		print one line, parse commands and other things in `{}`
		'''
		from translator import translator
		if s[0] == '#':
			return
		if s[0] == '{':
			parse(s)
		# story
		if skip or data.config['system']['printInterval'] <= 0:
			# pring line by once
			print(s, end='')
		else:
			# print line by char
			for c in s:
				print(c, end='', flush=True)
				sleep(data.config['system']['printInterval'] / 1000)