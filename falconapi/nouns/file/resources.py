import io
import os
import re
import uuid
import mimetypes
import collections
import json
import falcon
from falconapi.hooks.verification.hooks import authenticate
from falconapi.utilities.database.resources import insert_file, get_files
from falconapi.hooks.database.hooks import generate_cursor, kill_cursor


@falcon.before(generate_cursor)
@falcon.after(kill_cursor)
class FileCollection(object):

    def __init__(self, file_store):
        self._file_store = file_store

    def on_get(self, req, resp, username):
        self.cursor.callproc('fetch_files', [username])
        rows = self.cursor.fetchall()
        print(rows)
        objects_list = []
        for row in rows:
            dictionary = collections.OrderedDict()
            dictionary['id'] = row[0]['id']
            dictionary['user_id'] = row[0]['user_id']
            dictionary['uuidname'] = row[0]['uuidname']
            dictionary['filename'] = row[0]['filename']
            dictionary['username'] = row[0]['username']
            objects_list.append(dictionary)
        print(objects_list)
        resp.body = json.dumps(objects_list)
        resp.status = falcon.HTTP_200


    @falcon.before(authenticate)
    def on_post(self, req, resp, username):
        print(username)
        self.cursor.callproc('fetch_user', [username])
        result = self.cursor.fetchone()[0]
        user_id = result['id']
        file = req.get_param('file')
        print(req.content_type)
        print(file.type)
        filename = file.filename
        uuidname = self._file_store.save(file.file, file.type)
        self.cursor.callproc('insert_file', [user_id, uuidname, filename, username])
        resp.body = json.dumps(username)
        resp.status = falcon.HTTP_201

    def on_delete(self, req, resp):
        file = req.get_param('file')
        print(req.content_type)
        print(file.type)
        filename = file.filename
        name = self._file_store.delete(file.file, file.type)
        insert_file(self.cursor, filename, user, name)
        resp.status = falcon.HTTP_200
        resp.location = '/v1/api/files/' + name


class File(object):

    def __init__(self, file_store):
        self._file_store = file_store

    def on_get(self, req, resp, filename):
        resp.content_type = mimetypes.guess_type(filename)[0]
        resp.stream, resp.stream_len = self._file_store.open(filename)


class FileStore(object):

    _CHUNK_SIZE_BYTES = 4096
    _FILE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )

    def __init__(self, storage_path, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, file_stream, file_content_type):
        mimetypes.add_type('text/rtf', '.rtf', strict=True)
        ext = mimetypes.guess_extension(file_content_type)
        uuidname = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        file_path = os.path.join(self._storage_path, uuidname)

        with self._fopen(file_path, 'wb') as file:
            while True:
                chunk = file_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break
                file.write(chunk)
        return uuidname

    def open(self, filename):
        if not self._FILE_NAME_PATTERN.match(filename):
            raise IOError('File not found')
        file_path = os.path.join(self._storage_path, filename)
        stream = self._fopen(file_path, 'rb')
        stream_len = os.path.getsize(file_path)
        return stream, stream_len

    def delete(self, name):
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('File not found')
        path = os.path.join(self._storage_path, name)
        os.remove(path)
