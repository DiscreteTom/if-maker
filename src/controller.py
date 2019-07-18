import yaml
import os
from time import sleep
import data
import shell
import story
import readline

readline.parse_and_bind('tab: complete')
readline.set_completer(shell.completer)

def start():
	'''
	start project by calling `config['system.entry']`
	'''
	from translator import run
	run(data.config['system.entry'] + '()')

def newGame():
	'''
	start a new game, print story: `config['system.story.first']`, load data and loop
	'''
	story.printStory(data.config['system.story.first'])
	data.load()
	loop()

def loop():
	'''
	enable shell
	'''
	while True:
		s = input(data.config['system.shell.prefix'])
		if s == data.config['system']['shell']['exitCmd']:
			break
		if shell.parse(s) == False:
			print(data.config['system']['shell']['errorMsg'])

