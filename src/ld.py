'''
line discipline module
'''

import msvcrt
from data import data
import sys
import ctypes

# enable windows esc sequences
ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)

class lineDiscipline:
	@classmethod
	def getCmd(cls):
		from shell import shell
		cmd = ''
		while True:
			# print current command
			sys.stdout.write('\x1b[2K') # clear console last line
			print('\r', data.config['system.shell.prefix'], cmd, sep='', end='', flush=True)
			ch = msvcrt.getwch()
			if ch == '\r' or ch == '\n':
				print('')
				return cmd
			elif ch == '\t':
				# completion
				if cmd[-1] != ' ':
					cmds = cmd.split()
					rest = shell.getComletion(len(cmds), cmds[-1])
					cmd += rest
			elif ch == '\b':
				# backspace
				if len(cmd):
					cmd = cmd[:-1]
			else:
				# normal char
				cmd += ch;