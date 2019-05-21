from shell import shell
from data import data

class translator:
	@classmethod
	def run(cls, code: str):
		lines = code.split(';')
		result = None
		for line in lines:
			if len(line.strip()):
				result = eval(line.strip())
		return result
