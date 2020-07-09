import os
import hashlib

from config import ROOT_PATH


def get_hash(filepath, bufsize):
	""" Hash function of the file 

    :param filepath: path to the file.
    :type filepath: str

    :param bufsize: chunk to get the hash of the file.
    :type bufsize: int
	"""
	lib = hashlib.sha384()

	with open(filepath, 'rb') as f:
		while True:
			data = f.read(bufsize)
			if not data:
				break
			lib.update(data)

	return lib.hexdigest()


def check_root():
	""" Function for checking the presence of a folder for saving files """
	if not os.path.exists(ROOT_PATH):
		os.mkdir(ROOT_PATH)

