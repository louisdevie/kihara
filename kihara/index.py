from sys import argv, stdout
import re

from . import _locale
from .version import REPR
from . import utils

class KRIParsingError (SyntaxError): pass

KRI_BRANCH_TAG = re.compile(r'(\?)([a-z]+)(\[)')
KRI_LEAF_TAG = re.compile(r'(\!)([a-z]+)(\[)')

def main():
	argc = len(argv)
	if argc == 2:
		print(argv[1])
	elif argc == 3:
		if argv[1] == 'local':
			display_index(parse_index(load_local_index(argv[2])))
		else:
			_help_msg()
	else:
		_help_msg()

def _help_msg():
	print(f'kihara v{REPR}')
	print(_locale.INDEX_MODULE_HELP)

def display_index(index_data, indent=''):
	if isinstance(index_data, dict):
		for key, value in index_data.items():
			print(indent+key+':')
			display_index(value, indent+'  ')
	elif isinstance(index_data, list):
		for index, value in enumerate(index_data):
			print(indent+str(index+1)+':')
			display_index(value, indent+'  ')
	else:
		print(indent+repr(index_data))

def parse_index(text):
	parser = KRIParser(text)
	return parser.parse_global()

class KRIParser:
	def __init__(self, text):
		self.text = text
		self.head = 0
		self.EOF = len(self.text)
		self.tagname = None

	def on_branch_tag(self):
		match = KRI_BRANCH_TAG.match(self.text, self.head)
		if match:
			_, self.tagname, _ = match.groups()
			return True
		else:
			self.tagname = None
			return False

	def on_leaf_tag(self):
		match = KRI_LEAF_TAG.match(self.text, self.head)
		if match:
			_, self.tagname, _ = match.groups()
			return True
		else:
			self.tagname = None
			return False

	def on_tag_end(self):
		return self.text[self.head] == ']'

	def parse_global(self):
		data = dict()
		while True:
			if self.on_branch_tag():
				tagname = self.tagname
				self.head += len(tagname)+2
				data[tagname] = [self.parse_branch()]
			else:
				self.head += 1
			if self.head >= self.EOF:
				break
		return data

	def parse_branch(self):
		data = dict()
		while True:
			if self.on_leaf_tag():
				tagname = self.tagname
				self.head += len(tagname)+2
				if tagname in data.keys():
					data[tagname].append(self.parse_leaf())
				else:
					data[tagname] = [self.parse_leaf()]
			elif self.on_branch_tag():
				tagname = self.tagname
				self.head += len(tagname)+2
				if tagname in data.keys():
					data[tagname].append(self.parse_branch())
				else:
					data[tagname] = [self.parse_branch()]
			elif self.on_tag_end():
				self.head += 1
				break
			else:
				self.head += 1
			if self.head >= self.EOF:
				raise KRIParsingError(_locale.NO_MATCHING_BRACKET)
		return data

	def parse_leaf(self):
		data = str()
		while True:
			if self.on_tag_end():
				self.head += 1
				break
			else:
				data += self.text[self.head]
				self.head += 1
			if self.head >= self.EOF:
				raise KRIParsingError(_locale.NO_MATCHING_BRACKET)
		return data.strip()

def load_local_index(path):
	with open(path, 'rt', encoding='utf-8') as fd:
		content = fd.read()
	return content

if __name__ == '__main__':
	main()
