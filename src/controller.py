import yaml
import msvcrt
import os
from time import sleep
from data import data
from shell import shell
from story import story

class Controller:
	def start(self):
		# print welcome
		if 'welcome' in data.config['project']:
			print(data.config['project']['welcome'])
		else:
			print(data.config['project']['name'])

		# print main menu
		for i in range(len(data.config['mainMenu'])):
			print(i + 1, data.config['mainMenu'][i])

		# get user's choice
		index = 0
		while True:
			index = ord(msvcrt.getch()) - ord('0')
			if index in range(1, len(data.config['mainMenu']) + 1):
				break

		# os.system('cls') # clear the console

		# judge user input
		if data.config['mainMenu'][index - 1] == 'new':
			return self.newGame()
		elif data.config['mainMenu'][index - 1] == 'continue':
			return self.loop()
		elif data.config['mainMenu'][index - 1] == 'exit':
			return 0

	def newGame(self):
		story.tell(0)
		self.loop()

	def loop(self):
		while True:
			s = input(data.config['system']['shell']['prefix'])
			if s == data.config['system']['shell']['exitCmd']:
				break
			if shell.parse(s) == False:
				print(data.config['system']['shell']['errorMsg'])