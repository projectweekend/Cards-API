import falcon
from app import api
from app.utils.testing import APITestCase
from app.user import handlers as user_handlers


USER_COLLECTION_ROUTE = '/user'

VALID_DATA = {
    'email': 'test@test.com'
}

INVALID_DATA = {
    'NO_EMAIL': {},
    'BAD_EMAIL': {
        'email': 'not an email'
    }
}


class UserCollectionTestCase(APITestCase):

    def test_create_user(self):
        self.simulate_post(USER_COLLECTION_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

    def test_create_duplicate_user(self):
        self.simulate_post(USER_COLLECTION_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        self.simulate_post(USER_COLLECTION_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_CONFLICT)

    def test_create_user_with_invalid_data(self):
        body = self.simulate_post(USER_COLLECTION_ROUTE, INVALID_DATA['NO_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        print(body)
        error_keys = body['description'].keys()
        self.assertIn('email', error_keys)

        body = self.simulate_post(USER_COLLECTION_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        error_keys = body['description'].keys()
        self.assertIn('email', error_keys)
