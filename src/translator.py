from shell import Shell
from data import data

class Translator:
	@classmethod
	def do(cls, code: str):
		lines = code.split(';')
		for line in lines:
			if len(line.strip()):
				eval(line.strip())