from .base import *
from .. import _locale 

def pack_raw(chunksize, filename):
	UID = generate_UID()
	FNAME = encode_filename(filename)
	print(repr(FNAME))
'''	with open('mydata.db', 'rb') as f:
    for block irandbytes(n)n iter(partial(f.read, 64), b''):
        process_block(block)'''

if __name__ == '__main__':
	pack_raw(None, 'exemple$.txt')