from ifmCore import *
if len(sys.argv) == 1:
	print('usage: ifm {new|make|run|debug|package|clear} [projectName]\n')
	print('create a new project:')
	print('	ifm new [projectName]')
	print('')
	print('make the project in this folder:')
	print('	ifm make')
	print('')
	print('run your project:')
	print('	ifm run')
	print('')
	print('make and run your project:')
	print('	ifm debug')
	print('')
	print('package your project to an executable file:')
	print('	ifm package')
	print('')
	print('clear current project')
	print('	ifm clear')
elif sys.argv[1] == 'new':
	if len(sys.argv) > 2:
		new(sys.argv[2])
	new()
elif sys.argv[1] == 'make':
	make()
elif sys.argv[1] == 'run':
	import controller
	controller.start()
elif sys.argv[1] == 'debug':
	make()
	import controller
	controller.start()
elif sys.argv[1] == 'package':
	pass
elif sys.argv[1] == 'clear':
	clear()