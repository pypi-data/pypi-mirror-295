class Color:
	'''Takes an RGB sequence and converts it into both a background color and text color. Leave blank for no color.\n\nArguments:\n\tr-int, g-int, b-int, alpha-bool\nReturns:\n\tA color object.'''

	def __init__(self, r:int, g:int, b:int, alpha:bool=False):

		if (r > 255) or (g > 255) or (b > 255): # Raise exception if an RGB value exceeds 255
			raise Exception("RGB values cannot exceed 255")

		self.r = str(r)
		self.g = str(g)
		self.b = str(b)

		if alpha == False:
			self.background = f"\033[48;2;{r};{g};{b}m"
			self.fore = f"\033[38;2;{r};{g};{b}m"
		else:
			self.background = ""
			self.fore = ""

	

class Presets:
	BLACK = Color(0,0,0)
	RED = Color(200,0,0)
	YELLOW = Color(200,200,0)
	GREEN = Color(0,200,0)
	BLUE = Color(0,0,200)
	MAGENTA = Color(200,0,200)
	WHITE = Color(200,200,200)
	EMPTY = Color(0,0,0,True)