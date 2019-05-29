__if_flag = []

def run(code: str, params = {}):
	from shell import shell
	from data import data
	from story import story
	if 'debug.run' in data.config:
		print('debug.run: running', code, 'params:', params)
	cmds = code.replace('\n', ';').split(';')
	result = None
	for cmd in cmds:
		cmd = cmd.strip()
		if len(cmd) == 0:
			# empty command
			continue
		params['shell'] = shell
		params['data'] = data
		params['story'] = story

		# process if()/else/elif()/fi
		if cmd.startswith('if(') and cmd[-1] == ')':
			__if_flag.append(eval(cmd[3:-1]))
		elif cmd == 'else':
			__if_flag[-1] = not __if_flag[-1]
		elif cmd == 'fi':
			__if_flag.pop()
		elif cmd.startswith('elif(') and cmd[-1] == ')':
			__if_flag[-1] = eval(cmd[5:-1])
		elif len(__if_flag) == 0 or __if_flag[-1]:
			# run
			result = eval(preprocess(cmd), globals(), params)
	__if_flag.clear()
	return result

def preprocess(cmd: str):
	if cmd.startswith('load(') or cmd.startswith('unload(') or cmd.startswith('parse('):
		return 'shell.' + cmd
	if cmd.startswith('print(') or cmd.startswith('printStory(') or cmd.startswith('printItemList('):
		return 'story.' + cmd
	if cmd.startswith('findItem('):
		return 'data.' + cmd
	return cmd