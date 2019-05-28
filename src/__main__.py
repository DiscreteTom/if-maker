from ifm import *
from controller import Controller
if len(sys.argv) == 1:
	print('usage:\nifm [new|make]')
if sys.argv[1] == 'new':
	new()
elif sys.argv[1] == 'make':
	make()
elif sys.argv[1] == 'run':
	c = Controller()
	c.start()