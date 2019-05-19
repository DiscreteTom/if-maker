import yaml
import msvcrt
import os
from time import sleep
from data import data
from shell import shell

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
		# open story file
		f = open('../_stories/index.ift', encoding='utf-8')

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
			if line[0] != '{' and line[0] != '#':
				# not a command or a comment
				if data.config['system']['printInterval'] <= 0:
					# pring line by once
					print(line, end='')
				else:
					# print line by char
					for c in line:
						print(c, end='', flush=True)
						sleep(data.config['system']['printInterval'] / 1000)
				msvcrt.getch()

		self.loop()

	def loop(self):
		while True:
			s = input(data.config['system']['shell']['prefix'])
			if s == data.config['system']['shell']['exitCmd']:
				break
			if shell.parse(s) == False:
				print(data.config['system']['shell']['errorMsg'])




if __name__ == '__main__':
	c = Controller()
	c.start()