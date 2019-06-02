'''
line discipline module
'''

import msvcrt

class lineDiscipline:
	@classmethod
	def getCmd(cls):
		from shell import shell
		cmd = ''
		while True:
			ch = msvcrt.getwch()
			if ch == '\r' or ch == '\n':
				print('')
				return cmd
			elif ch == '\t':
				# completion
				if cmd[-1] != ' ':
					cmds = cmd.split()
					rest = shell.getComletion(len(cmds), cmds[-1])
					cmd += rest + ' '
					print(rest, end=' ', flush=True)
			elif ch == '\b':
				# backspace
				if len(cmd):
					cmd = cmd[:-1]
					print('\b \b', end='', flush=True)
			else:
				# normal char
				cmd += ch;
				print(ch, end='', flush=True)