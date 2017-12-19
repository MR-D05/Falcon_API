import os
import falcon
from falcon_cors import CORS
from falconapi.middleware.middleware import Middleware
from falconapi.nouns.user.resources import UserCollection, PasswordResource, PasswordResetRequestResource
from falconapi.nouns.file.resources import FileCollection, File, FileStore
from falcon_multipart.middleware import MultipartMiddleware

cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)

def create_app(file_store):
    middleware = [Middleware(), MultipartMiddleware()]
    api = falcon.API(middleware=middleware)
    api.add_route('/v1/api/users', UserCollection())
    api.add_route('/v1/api/password-reset-request', PasswordResetRequestResource())
    api.add_route('/v1/api/password-reset', PasswordResource())
    api.add_route('/v1/api/{username}/files', FileCollection(file_store))
    api.add_route('/v1/api/files/{filename}', File(file_store))
    return api

def get_app():
    storage_path = os.environ.get('APP_STORAGE_PATH')
    file_store = FileStore(storage_path)
    return create_app(file_store)