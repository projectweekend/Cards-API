import falcon
from app.utils.testing import AuthenticatedAPITestCase


DECK_COLLECTION_ROUTE = '/deck'

VALID_DATA = {
    'count': 1
}

INVALID_DATA = {
    'NO_COUNT': {},
    'BAD_COUNT': {
        'count': 'not int'
    }
}


class DeckCollectionTestCase(AuthenticatedAPITestCase):

    def test_create_deck(self):
        body = self.simulate_post(
            DECK_COLLECTION_ROUTE,
            VALID_DATA,
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)
        self.assertIn('id', body.keys())
        self.assertEqual(len(body['cards']), 52)
        self.assertEqual(body['groups'], {})
        card = body['cards'][0]
        self.assertIn('rank', card.keys())
        self.assertIn('suit', card.keys())
        self.assertIn('front', card.keys())
        self.assertIn('back', card.keys())

    def test_create_without_api_key(self):
        self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_UNAUTHORIZED)

    def test_create_deck_with_invalid_data(self):
        body = self.simulate_post(
            DECK_COLLECTION_ROUTE,
            INVALID_DATA['NO_COUNT'],
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        error_keys = body['description'].keys()
        self.assertIn('count', error_keys)

        body = self.simulate_post(
            DECK_COLLECTION_ROUTE,
            INVALID_DATA['BAD_COUNT'],
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        error_keys = body['description'].keys()
        self.assertIn('count', error_keys)
