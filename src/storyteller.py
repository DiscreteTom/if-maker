import re
from data import data
import msvcrt
from time import sleep

class StoryTeller:
	@classmethod
	def tell(cls, story_id):
		'''
		return False if story_id is not found in story file. story_id could be a number or a string
		'''
		f = open('../_stories/index.ift', encoding='utf-8')
		# find the story
		while True:
			s = f.readline()
			if len(s) == 0:
				# EOF without finding out the story
				return False
			# use regex to find story token
			match = re.search('\\{(\\d+)\\s*(:\\s*([^}]+))?\\}', s)
			if match:
				if str(story_id) == match.group(1) or story_id == match.group(3):
					break
		# print the story
		skip = False
		while True:
			s = f.readline()
			if len(s) == 0 or s == '\n':
				# EOF or end of story
				return True
			if s[0] == '#':
				# comment
				continue
			if s[0] == '{':
				cls.__parseCmd(s)
				continue
			# story
			if skip or data.config['system']['printInterval'] <= 0:
				# pring line by once
				print(s, end='')
			else:
				# print line by char
				for c in s:
					print(c, end='', flush=True)
					sleep(data.config['system']['printInterval'] / 1000)
			if not skip:
				if msvcrt.getwch() == '\u001B':
					# if `esc` is pressed
					skip = True

	@classmethod
	def __parseCmd(cls, s: str):
		'''
		parse command in story, format: `{operation: value}`
		'''
		from translator import Translator
		match = re.search('\\{([^}:]+)\\s*(:\\s*([^}]+))?\\}', s)
		op = match.group(1)
		value = match.group(3)
		if op == 'bgm':
			pass
		elif op == 'call':
			pass
		elif op == 'code':
			Translator.do(value)