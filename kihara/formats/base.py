import functools, random

__all__ = [
	'randbytes', 'functools'
]

SAFE_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-.'

def randbytes(n):
	return bytes([random.randint(0, 255) for i in range(n)])

def generate_UID():
	return randbytes(8)

def encode_filename(filename):
	encoded = bytes()
	warn = False
	overflow = False
	while True:
		if filename:
			char, filename = filename[0], filename[1:]
			if (not char in SAFE_CHARS):
				warn = True
			char = char.encode('utf-8')
		else:
			break
		if len(encoded)+len(char) > 42:
			overflow = True
			break
		else:
			encoded += char
			if len(encoded) == 42:
				break
	if warn:
		print(_locale.FILENAME_CHARS_WARNING)
	return encoded
