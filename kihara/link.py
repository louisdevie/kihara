'''
KLinks manipulation

kLink is a compressed base64 encoding optimized for URLs.
'''

from sys import argv

from . import _locale
from .version import REPR
from . import utils

PROTOCOLS = utils.TwoWayMap(
	('',      b'\xe0'), # 111
	('http',  b'\x20'), # 001
	('https', b'\xa0'), # 101
	('ftp',   b'\x00'), # 000
	('ftps',  b'\x80'), # 100
	('sftp',  b'\x40'), # 010
)

PROTOCOL_SEPARATOR = '://'

BASE64_TABLE = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
	'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
	'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
	'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
	'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
	'w', 'x', 'y', 'z', '0', '1', '2', '3',
	'4', '5', '6', '7', '8', '9', '+', '_',
]

PADDING_FLAG_CHAR = '!'

KIHARA_LINK_CODE = [
	[
		'!', '?', '&', '$', '#', '%', '*', '+', '-', '.', '/', '@', ':', '_',
		'(', ')', '[', ']', '{', '}', '|', '^', '~', '=', '<', '>', ',', ';'],
	[
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
		'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-'],
	[
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
		'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '+', '_'],
	[
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '`', '\\', '\'', '"',
		' ', '+', '?', ':', ';', ',', '%', '-', '_', '@', '=', '&', '#', '.']
]

def main():
	argc = len(argv)
	if argc == 3:
		if argv[1] == 'geturl':
			print(get_url(utils.trim_quotes(argv[2])))
		elif argv[1] == 'makelink':
			print(make_link(utils.trim_quotes(argv[2])))
		else:
			_help_msg()
	else:
		_help_msg() 

def _help_msg():
	print(f'kihara v{REPR}')
	print(_locale.LINK_MODULE_HELP)

def make_link(url):
	'''
	Create a kLink from the given URL.

	The URL can be anything composed of printable ascii charaters.
	(for example, 'https://awebsite.com' and  'Hello, World!' are both valid)
	'''
	if url.count(PROTOCOL_SEPARATOR) == 0:
		protocol = ''
		location = url
	else:
		protocol, location = url.split(PROTOCOL_SEPARATOR, 1)
		if not protocol in PROTOCOLS.left:
			protocol = ''
			location = url

	encoder = KLinkEncoder()

	encoder.write(PROTOCOLS.left[protocol], 3)

	mode = 1
	for char in location:
		if char in KIHARA_LINK_CODE[mode]:
			encoder.write(
				bytes(
					[KIHARA_LINK_CODE[mode].index(char) << 3]
				), 5)
		else:
			for i in range(4):
				if char in KIHARA_LINK_CODE[i]:
					mode = i
					encoder.write(bytes([(mode+28) << 3]), 5)
					encoder.write(
						bytes(
							[KIHARA_LINK_CODE[mode].index(char) << 3]
						), 5)
					break
			else:
				raise ValueError(_locale.INVALID_URL)

	encoder.pad()

	return encoder.read()

def get_url(link):
	'''
	extract the URL from a kLink.
	'''
	if link.endswith(PADDING_FLAG_CHAR):
		padded = False
		link = link[:-1]
	else:
		padded = True

	decoder = KLinkDecoder()

	for char in link:
		if char in BASE64_TABLE:
			decoder.write(
				bytes(
					[BASE64_TABLE.index(char) << 2]
				), 6)
		else:
			raise ValueError(_locale.INVALID_LINK)

	if padded:
		decoder.remove_padding()
			
	protocol = bytes(decoder.read(1), 'latin-1')

	if protocol == b'\xe0':
		return decoder.read()
	elif protocol in PROTOCOLS.right:
		return PROTOCOL_SEPARATOR.join((PROTOCOLS.right[protocol], decoder.read()))
	else:
		raise ValueError(_locale.INVALID_LINK)

class KLinkBaseCoDec:
	def __init__(self):
		self.outputbuffer = str()
		self.inputbuffer = 0

	def _write_bit(self, bit):
		raise NotImplementedError

	def write(self, data, stop):
		written = 0
		for byte in data:
			for i in range(7, -1, -1):
				bit = 1 if byte & (2**i) else 0
				self._write_bit(bit)
				written += 1
				if written == stop:
					break
			if written == stop:
				break

	def read(self, maxsize=-1):
		if maxsize == -1:
			output = self.outputbuffer[:]			
			self.outputbuffer = str()
		else:
			output = self.outputbuffer[:maxsize]
			self.outputbuffer = self.outputbuffer[maxsize:]
		return output

class KLinkEncoder (KLinkBaseCoDec):
	def __init__(self):
		super().__init__()
		self.inputfill = 5

	def _write_bit(self, bit):
		self.inputbuffer += bit << self.inputfill
		self.inputfill -= 1
		if self.inputfill == -1:
			self.outputbuffer += BASE64_TABLE[self.inputbuffer]
			self.inputbuffer = 0
			self.inputfill = 5

	def pad(self):
		if self.inputfill != 5:
			for i in range(self.inputfill+1):
				self._write_bit(0)
		else:
			self.outputbuffer += PADDING_FLAG_CHAR

class KLinkDecoder (KLinkBaseCoDec):
	def __init__(self):
		super().__init__()
		self.inputfill = 2
		self.mode = -1

	def _write_bit(self, bit):
		self.inputbuffer += bit << self.inputfill
		self.inputfill -= 1
		if self.inputfill == -1:
			if self.mode == -1:
				self.outputbuffer += chr(self.inputbuffer << 5)
				self.mode = 1
			else:
				if self.inputbuffer < 28:
					self.outputbuffer += KIHARA_LINK_CODE[self.mode][self.inputbuffer]
				else:
					self.mode = self.inputbuffer-28
			self.inputbuffer = 0
			self.inputfill = 4

	def remove_padding(self):
		if self.inputfill == 4:
			self.outputbuffer = self.outputbuffer[:-1]

if __name__ == '__main__':
	main()