import falcon
import json
from app.config import DATABASE_URL
from app.app import get_app, create_app
from tests.app_test_case import AppTestCase

HEADERS = {'Content-Type': 'application/json'}

USER_RESOURCE_ROUTE = '/v1/api/users'

VALID_ADMIN = {'Name': 'admin', 'Password': 'adminpassword'}

VALID_USER = {'Name': 'john', 'Password': 'testpassword123'}

INVALID_DATA = {
    'MISSING_USERNAME': {
        'password': 'password'
    },
    'BAD_USERNAME': {
        'username': 'badusername',
        'password': 'password'
    },
    'MISSING_PASSWORD': {
        'username': 'username'
    },
    'BAD_PASSWORD': {
        'username': 'john',
        'password': 'badpassword'
    },
    'DOES_NOT_EXIST': {
        'username': 'intruder',
        'password': 'doesntmatter'
    }
}


class UserResourcesTest(AppTestCase):

    def test_login(self):
        body = self.simulate_post(
            path=USER_RESOURCE_ROUTE, headers=HEADERS, body=json.dumps(VALID_USER))
        self.assertEqual(body.status, falcon.HTTP_200)
        self.assertNotEqual(len(body.cookies), 0)
