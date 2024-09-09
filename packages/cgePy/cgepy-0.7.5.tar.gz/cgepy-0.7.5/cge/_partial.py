from ._screenclear import Clear

def out(ctx, clearingmethod: int = 1):
	"""Higher resolution canvas output using unicode half-blocks.\nNote that index zero of your canvas will define the length of all other indexes."""

	Clear(clearingmethod)

	buffer = ""
	index_i = -2

	for i in range(len(ctx)//2):
		index_j = -1
		index_i += 2

		for j in range(len(ctx[0])):
			index_j += 1

			j = ctx[index_i][index_j].fore + ctx[index_i+1][index_j].background + '▀'
			buffer += j

		buffer += '\033[0m\n'

	print(buffer)