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
        self.simulate_post(DECK_COLLECTION_ROUTE, INVALID_DATA, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    def test_list_decks(self):
        # create a deck first
        self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        # get a list of decks
        body = self.simulate_get(DECK_COLLECTION_ROUTE, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(len(body), 1)

        deck = body[0]
        self.assertIn('id', deck)
        self.assertEqual(deck['remaining'], 52)
        self.assertEqual(deck['removed'], 0)
