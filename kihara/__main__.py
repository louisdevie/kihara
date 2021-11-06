from .version import REPR
from . import _locale

def main():
	print(f'kihara v{REPR}')
	print(_locale.MAIN_INFO_MSG)

if __name__ == '__main__':
	main()