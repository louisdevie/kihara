from .base import *

def pack_raw(chunksize, filepath):
	filename = os.path.split(filepath)[1]
	UID = generate_UID()
	FNAME = encode_filename(filename)

	with open(f'{os.path.splitext(filename)[0]}.khr', 'wb+') as fdout:
		fdout.write(FNAME)
		fdout.write(UID)
		fdout.write(bytes(14))

		checksum = hashlib.sha256()

		with open(filepath, 'rb') as fdin:
			while block := fdin.read(CHUNK_SIZE):
				checksum.update(block)
				fdout.write(block)

		print(checksum.hexdigest())
		fdout.seek(50, 0)
		fdout.write(checksum.digest()[:8])

if __name__ == '__main__':
	pack_raw(-1, 'exemple.txt')