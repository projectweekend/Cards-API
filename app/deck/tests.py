import falcon
from app.utils.testing import AuthenticatedAPITestCase


DECK_COLLECTION_ROUTE = '/deck'

VALID_DATA = {
    'count': 1
}

INVALID_DATA = {
    'count': 'abc'
}


class DeckCollectionTestCase(AuthenticatedAPITestCase):

    def test_create_a_deck(self):
        body = self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertIn('id', body)
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

    def test_create_a_deck_with_invalid_data(self):
        body = self.simulate_post(DECK_COLLECTION_ROUTE, INVALID_DATA, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        # self.assertNotEqual(len(body['token']), 0)
