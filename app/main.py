import os
from pathlib import Path
import shutil
import json
from bottle import error, run, get, post, delete, request, response, static_file
from bottledaemon import daemon_run

from config import ROOT_PATH, HOST, PORT
from services import check_root, get_hash


@get('/download')
def get_file():
    """ Processing a file download request """

    file_hash = request.query.get('h')
    if not file_hash:
        return {'status': 'fail', 'error': 'have no h parameter'}

    try:
        find_dir = os.path.join(ROOT_PATH, file_hash[:2])
        file = [file for file in os.listdir(find_dir) if file.split('.')[0] == file_hash][0]
        return static_file(file, root=find_dir, download=file)
    except (IndexError, FileNotFoundError):
        return {'status': 'fail', 'error': 'file does not exists'}


@post('/upload')
def upload_file():
    """ Processing a file upload request """

    try:
        upload = request.files.get('file')
        file_hash = get_hash(upload)
        save_dir = os.path.join(ROOT_PATH, file_hash[:2])

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        upload.save(os.path.join(save_dir, file_hash + Path(upload.filename).suffix))
        return {'result': 'success', 'message': 'file has been saved', 'hash': file_hash}
    except OSError:
        return {'result': 'unsuccess', 'message': 'file exists'}

    except AttributeError:
        return  {'result': 'unsuccess', 'message': 'there is no file key or cannot find the file'}


@delete('/remove')
def remove_file():
    """ Processing a request to delete a file """

    file_hash = request.query.get('h')
    if not file_hash:
        return {'result': 'fail', 'error': 'there is no parameter named h'}

    try:
        find_dir = os.path.join(ROOT_PATH, file_hash[:2])
        file = [file for file in os.listdir(find_dir) if file.split('.')[0] == file_hash][0]
        os.remove(os.path.join(find_dir, file))
        if not os.listdir(find_dir):
            os.rmdir(find_dir)
        return {'result': 'success', 'message': 'file successfully delete'}

    except (IndexError, FileNotFoundError):
        return {'result': 'fail', 'error': 'file does not exists'}


@error(404)
def error404(error):
    response.content_type = 'application/json'
    return json.dumps({'result': 'fail', 'error': 'there is no route like this'})


@error(500)
def error500(error):
    response.content_type = 'application/json'
    return json.dumps({'result': 'fail', 'error': 'internal server error, something goes wrong'})


if __name__ == '__main__':
    check_root()
    daemon_run(host=HOST, port=PORT)

