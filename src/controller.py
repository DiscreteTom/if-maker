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
	# print welcome
	if 'project.welcome' in data.config:
		print(data.config['project.welcome'])
	else:
		print(data.config['project.name'])

	# print main menu
	for i in range(len(data.config['mainMenu'])):
		print(i + 1, data.config['mainMenu'][i])

	# get user's choice
	index = 0
	while True:
		index = ord(msvcrt.getch()) - ord('0')
		if index in range(1, len(data.config['mainMenu']) + 1):
			break

	# judge user input
	if data.config['mainMenu'][index - 1] == 'new':
		return newGame()
	elif data.config['mainMenu'][index - 1] == 'continue':
		return loop()
	elif data.config['mainMenu'][index - 1] == 'exit':
		return 0

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

