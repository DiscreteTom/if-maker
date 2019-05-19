import yaml
import msvcrt
import os
from time import sleep

class Controller:
	config = None
	def __init__(self):
		'load config msg from _config.yml'
		f = open('_config.yml', 'r')
		self.config = yaml.load(f)
	
	def start(self):
		# print welcome
		if 'welcome' in self.config['project']:
			print(self.config['project']['welcome'])
		else:
			print(self.config['project']['name'])

		# print main menu
		for i in range(len(self.config['mainMenu'])):
			print(i + 1, self.config['mainMenu'][i])

		# get user's choice
		index = 0
		while True:
			index = ord(msvcrt.getch()) - ord('0')
			if index in range(1, len(self.config['mainMenu']) + 1):
				break

		# os.system('cls') # clear the console

		# judge user input
		if self.config['mainMenu'][index - 1] == 'new':
			return self.newGame()
		elif self.config['mainMenu'][index - 1] == 'continue':
			return self.continueGame()
		elif self.config['mainMenu'][index - 1] == 'exit':
			return 0

	def newGame(self):
		# open story file
		f = open('_stories/main.ift', encoding='utf-8')

		# find the first story
		line = ''
		while True:
			line = f.readline() # include '\n'
			if len(line) == 0:
				# EOF without finding the first story
				return 1
			if line == '{0}\n':
				break

		# now we find the '{0}'
		while True:
			line = f.readline()
			if len(line) == 0 or line == '\n':
				#EOF or end of story
				break
			if line[0] != '{':
				# not a command
				if self.config['system']['printInterval'] <= 0:
					# pring line by once
					print(line, end='')
				else:
					# print line by char
					for c in line:
						print(c, end='', flush=True)
						sleep(self.config['system']['printInterval'] / 1000)
				msvcrt.getch()

		self.shell()

	def continueGame(self):
		self.shell()

	def shell(self):
		print(self.config['system']['shellPrefix'], end='')
		return



if __name__ == '__main__':
	c = Controller()
	c.start()