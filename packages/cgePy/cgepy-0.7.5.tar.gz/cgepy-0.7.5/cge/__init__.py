__version__ = "0.7.5"

# Import required modules

from .colors import Presets
from ._partial import out
from ._exceptions import Exceptions
from ._screenclear import ClearingMethod
from .ext import clear

# Defualt settings

spritecolor = Presets.RED
background = Presets.BLUE

# Classes

class Grid:

	def __init__(self, size:int = 20):
		self.sprites = []
		self.size = size

		self.ctx = [[background for i in range(self.size)] for i in range(self.size)]


	def Clear(self):
		"""Clears the grid context. Does not erase sprites."""
		self.ctx = [[background for i in range(self.size)] for i in range(self.size)]
		
	def Write(self, pos, new):
		"""Change the color value of a position on the grid."""
		try:
			self.ctx[pos[1]][pos[0]] = new

		except IndexError:
			e = "Grid index out of range"
			raise Exceptions.GridError(e)
		
	def w(self, pos, new):
		"""Shortcut method for Grid.Write()"""
		self.Write(pos, new)

	def Update(self, clearingmethod:ClearingMethod = ClearingMethod.STANDARD):
		"""Prints the grid to the screen using a buffer."""

		tmp = self.ctx.copy()

		if self.sprites != []:

			for sprite in self.sprites:
				tmp[sprite.pos[1]][sprite.pos[0]] = sprite.color

		if len(tmp)%2 == 1:
			tmp.append([Presets.EMPTY for i in range(self.size)])
		
		out(tmp, clearingmethod)  

class Sprite:

	def __init__(self, pos = (0,0), color = spritecolor):
		self.pos = pos
		self.color = color

	def Move(self, dir:str):
		if dir.lower() in ["up","w","i","\x1b[A","north"]:
			self.pos[1] -= 1
		if dir.lower() in ["down","s","k","\x1b[B","south"]:
			self.pos[1] += 1
		if dir.lower() in ["left","a","j","\x1b[D","west"]:
			self.pos[0] -= 1
		if dir.lower() in ["right","d","l","\x1b[C","east"]:
			self.pos[0] += 1

	def Go(self, pos = (0,0)):
		self.pos = pos

	def Drop(self, grid):
		grid.sprites.append(self)
	def Remove(self, grid):
		grid.sprites.remove(self)
