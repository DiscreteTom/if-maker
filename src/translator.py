from shell import mount, unmount, parse, loadedItems
from data import config, items, game, completer, findItem, save, load
from story import printf, printStory, printItemList
from controller import start, newGame, loop
from output import *

def run(code: str, params = {}):
	'''
	run `code` in ifm environment
	'''
	# remove empty lines
	codes = code.split('\n')
	code = ''
	for line in codes:
		if line.strip() != '':
			code += line + '\n'

	if code == '':
		# empty code
		return

	# process code, remove indent
	codes = code.split('\n')
	while codes[0][0] in [' ', '	']:
		for i in range(len(codes)):
			codes[i] = codes[i][1:]
	code = '\n'.join(codes)

	# run code
	if 'debug.run' in config:
		print('debug.run: running', code, 'params:', params)
	exec(code, globals(), params)
	return
