import yaml
import msvcrt
import os
from time import sleep
from data import data
from shell import shell, completer
from story import story
import readline

readline.parse_and_bind('tab: complete')
readline.set_completer(completer)

def start():
	from translator import run
	run(data.config['system.entry'] + '()')

def newGame():
	story.printStory(data.config['system.story.first'])
	loop()

def loop():
	while True:
		s = input(data.config['system.shell.prefix'])
		if s == data.config['system']['shell']['exitCmd']:
			break
		if shell.parse(s) == False:
			print(data.config['system']['shell']['errorMsg'])

