import re
import requests
import os
from sys import argv
from datetime import datetime

from . import _locale
from . import _cachedir
from . import utils
from .version import REPR
from .link import get_url

class KRIParsingError (SyntaxError): pass

KRI_BRANCH_TAG = re.compile(r'(\?)(resource|version|fragment)(\[)')
KRI_LEAF_TAG = re.compile(r'(!)(name|size|type|description|provider|location)(\[)')

def main():
	argc = len(argv)
	if argc == 2:
		link = utils.trim_quotes(argv[1])
		url = get_url(link)
		print(_locale.REMOTE_INDEX.format(url))
		display_index(parse_index(load_remote_index(url, link)))
	elif argc == 3:
		if argv[1] == 'local':
			path = utils.trim_quotes(argv[2])
			print(_locale.LOCAL_INDEX.format(path))
			display_index(parse_index(load_local_index(path)))
		elif argv[21] == 'nocache':
			link = utils.trim_quotes(argv[2])
			url = get_url(link)
			print(_locale.REMOTE_INDEX.format(url))
			display_index(parse_index(load_remote_index(url, link, False)))
		else:
			_help_msg()
	else:
		_help_msg()

def _help_msg():
	print(f'kihara v{REPR}')
	print(_locale.INDEX_MODULE_HELP)

def display_index(index_data):
	print(_locale.INDEX_INFO)

	if not 'resource' in index_data:
		printfield(_locale.INDEX_NO_RESOURCE)
		return
	res = index_data.get('resource')[0]

	printfield(
		res.get('name',	[_locale.INDEX_UNKNOWN_FIELD])[0],
		_locale.INDEX_NAME  )
	printfield(
		res.get('description', [_locale.INDEX_UNKNOWN_FIELD])[0],
		_locale.INDEX_DESCRIPTION  )
	printfield(
		res.get('provider', [_locale.INDEX_UNKNOWN_FIELD])[0],
		_locale.INDEX_RESOURCE_PROVIDER  )

	for i, ver in enumerate(res.get('version', [])):
		printfield(
			'',
			_locale.INDEX_VERSION.format(i+1)  )
		printfield(
			ver.get('name', [_locale.INDEX_UNKNOWN_FIELD])[0],
			_locale.INDEX_NAME, 2)
		printfield(
			ver.get('description', [_locale.INDEX_UNKNOWN_FIELD])[0],
			_locale.INDEX_DESCRIPTION, 2)
		printfield(
			res.get('provider', [_locale.INDEX_UNKNOWN_FIELD])[0],
			_locale.INDEX_LOCATION_PROVIDER, 2)
		printfield(
			humanize_file_size(ver.get('size', [_locale.INDEX_UNKNOWN_FIELD])[0]),
			_locale.INDEX_SIZE, 2)
		for i, frag in enumerate(ver.get('fragment', [])):
			printfield(
				'',
				_locale.INDEX_FRAGMENT.format(i+1), 2)
			printfield(
				type_name(frag.get('type', [_locale.INDEX_UNKNOWN_FIELD])[0]),
				_locale.INDEX_TYPE, 3)
			printfield(
				frag.get('location', [_locale.INDEX_UNKNOWN_FIELD])[0],
				_locale.INDEX_LOCATION, 3)

def printfield(value, name='', indent=1):
	if name: name += ' '
	value = value.split('\n')
	base_indent = '   '*indent
	val_indent = base_indent + ' '*len(name)
	for i, l in enumerate(value):
		if i == 0:
			print(base_indent+name+l)
		else:
			print(val_indent+l)

SIZE_UNITS = ('o', 'kio', 'Mio', 'Gio')

def humanize_file_size(size):
	size = float(int(size))
	unit = 0
	while size > 2048 and unit < 3:
		size /= 1024
		unit += 1
	return str(round(size, 1))+' '+SIZE_UNITS[unit]

LOCATION_TYPES = {
	'https': 'INDEX_HTTPS_LOCATION',
	'http': 'INDEX_HTTP_LOCATION',
	'gdrive': 'INDEX_GOOGLE_DRIVE_LOCATION'
}

def type_name(typeid):
	return _locale.TEXT[LOCATION_TYPES.get(typeid, 'INDEX_UNKNOWN_FIELD')]

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
		content = fd.readlines()
	return '\n'.join([line.strip() for line in content])

def load_remote_index(url, link, usecache=True):
	cache = _cachedir.user_cache_path(link+'{0.year:04}{0.month:02}{0.day:02}{0.hour:02}'.format(datetime.now()))
	_clear_old_cache()
	if usecache and os.path.isfile(cache):
		with open(cache, 'rt', encoding='utf-8') as fd:
			content = fd.readlines()
	else:
		r = requests.get(url)
		r.raise_for_status()
		with open(cache, 'wt+', encoding='utf-8') as fd:
			fd.write(r.text)
		content = r.text.split('\n')
	return '\n'.join([line.strip() for line in content])

def _clear_old_cache():
	today = '{0.year:04}{0.month:02}{0.day:02}'.format(datetime.now())
	cachedir = _cachedir.user_cache_path('')
	for fname in os.listdir(cachedir):
		date = fname[-10:-2]
		if date != today:
			os.remove(os.path.join(cachedir, fname))

def generate_code(index_data):
	text = str()
	for tag, data in index_data.items():
		if isinstance(data[0], str):
			for value in data:
				text += '!' + tag + '[' + value + ']'
		else:
			for value in data:
				text += '?' + tag + '[' + generate_code(value) + ']'
	return text

if __name__ == '__main__':
	main()