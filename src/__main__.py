from ifm import *
if len(sys.argv) == 1:
	print('usage:\nifm [new|make|run|debug]')
if sys.argv[1] == 'new':
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