from enum import Enum

class ClearingMethod(Enum):
	STANDARD = 1
	NONE = 2
	COMPACT = 3

def Clear(method: ClearingMethod = 1, gridsize: int = 20):

	if method == 1:

		print('\033[0;0H',end='')
		print('\033[2J',end='')

	elif method == 2:

		pass

	elif method == 3:

		from math import ceil
		for row in range(ceil(gridsize/2)):
			print('\033[1F',end='')
			print('\033[2K',end='')

	else:

		print('\033[0;0H',end='')
		print('\033[2J',end='')