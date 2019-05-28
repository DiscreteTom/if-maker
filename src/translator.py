class translator:
	@classmethod
	def run(cls, code: str, params = {}):
		from shell import shell
		from data import data
		cmds = code.split(';')
		for cmd in cmds:
			cmd = cmd.strip()
			if len(cmd) == 0:
				# empty command
				continue
			result = eval(preprocess(cmd), globals(), params)
		return result

	@classmethod
	def preprocess(cls, cmd: str):
		if cmd.startswith('load(') or cmd.startswith('unload(') or cmd.startswith('parse('):
			return 'shell.' + cmd
		if cmd.startswith('print(') or cmd.startswith('printStory('):
			return 'story.' + cmd
		if cmd.startswith('findItem('):
			return 'data.' + cmd
		return cmd