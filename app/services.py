import os
import hashlib
from io import BytesIO
from pathlib import Path

from config import ROOT_PATH


def get_hash(file):
    """ Get a hash of the file """

    file_bytes = BytesIO()
    file.save(file_bytes, Path(file.filename).suffix)
    file_hash = hashlib.sha384(file_bytes.getbuffer()).hexdigest()
    return file_hash


def check_root():
    """ Function for checking the presence of a folder for saving files """
    if not os.path.exists(ROOT_PATH):
        os.mkdir(ROOT_PATH)
        