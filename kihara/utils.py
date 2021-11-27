def trim_quotes(arg):
	'''
	trim quotes in command-line arguments
	'''
	if arg.startswith('"') or arg.startswith("'"):
		arg = arg[1:]
	if arg.endswith('"') or arg.endswith("'"):
		arg = arg[:-1]
	return arg

class TwoWayMap:
	def __init__(self, *couples):
		self.left = dict()
		self.right = dict()
		for c in couples:
			self.left[c[0]] = c[1]
			self.right[c[1]] = c[0]