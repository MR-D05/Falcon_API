import falcon
from cerberus import Validator
from falconapi.utilities.token.resources import generate_token
from falconapi.utilities.password.resources import verify


FIELDS = {
    'email': {
        'type': 'string',
        'regex': '^[^@]+@[^@]+\.[^@]+$',
        'required': True
    },
    'username': {
        'type': 'string',
        'required': True
    },
    'password': {
        'type': 'string',
        'required': True,
        'minlength': 12
    },
}


def validate(req, resp, resource, params):
    schema = {
        'email_address': FIELDS['email'],
        'username': FIELDS['username'],
        'password': FIELDS['password']
    }
    try:
        v = Validator(schema)
        if not v.validate(req.context['d']):
            raise falcon.HTTPBadRequest('Bad request', v.errors)
    except (TypeError):
            raise falcon.HTTPBadRequest
                 

def authenticate(req, resp, resource, params):
    try:
        token = req.cookies['SSSNTKN']
        resource.cursor.callproc('fetch_token', [token])
        result = resource.cursor.fetchone()[0]
    except (TypeError, KeyError):
        try:
            username = req.context['d']['username']
            password = req.context['d']['password']
            resource.cursor.callproc('fetch_user', [username])
            result = resource.cursor.fetchone()[0]
            encrypted_password = result['encrypted_password']
            valid_password = verify(password, encrypted_password)
            if not valid_password:
                raise falcon.HTTPBadRequest
        except (TypeError, KeyError):
            raise falcon.HTTPBadRequest
    finally:
        try:
            if len(req.cookies) == 0:
                username = req.context['d']['username']
                resource.cursor.callproc('fetch_user', [username])
                result = resource.cursor.fetchone()[0]
                id = result['id']
                token = generate_token(128)
                resource.cursor.callproc('insert_token', [id, token])
                resp.set_cookie("SSSNTKN", token, secure=False)
        except (TypeError, KeyError):
            raise falcon.HTTPBadRequest