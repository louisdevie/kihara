from sys import argv

from . import _locale
from .version import REPR
from . import utils
from .formats.raw import pack_raw

def main():
	argc = len(argv)
	if argc > 2:
		output_format = argv[1]
		if argc == 3:
			chunk_size = -1
			input_file = argv[2]
		elif argc == 4:
			if not argv[2].isdigit():
				_help_msg()
				return 1
			chunk_size = int(argv[2])
			input_file = argv[3]
		else:
			_help_msg()
			return 1
		if output_format == 'raw':
			pack_raw(chunk_size, input_file)
		else:
			_help_msg()
			return 1	
	else:
		_help_msg()
		return 1

def _help_msg():
	print(f'kihara v{REPR}')
	print(_locale.PACK_MODULE_HELP)

if __name__ == '__main__':
	main()