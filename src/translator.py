from shell import Shell
from data import data

class Translator:
	@classmethod
	def do(cls, code: str):
		lines = code.split(';')
		result = None
		for line in lines:
			if len(line.strip()):
				result = eval(line.strip())
		return result
