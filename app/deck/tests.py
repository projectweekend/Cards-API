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


class DeckItemTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(DeckItemTestCase, self).setUp()
        body = self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.deck_id = body['id']
        self.deck_item_route = '{0}/{1}'.format(DECK_COLLECTION_ROUTE, self.deck_id)
        self.deck_item_route_not_exists = '{0}/9999999'.format(DECK_COLLECTION_ROUTE)

    def test_get_deck(self):
        body = self.simulate_get(self.deck_item_route, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['id'], self.deck_id)
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

    def test_get_deck_not_exists(self):
        self.simulate_get(self.deck_item_route_not_exists, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_404)

    def test_delete_deck(self):
        self.simulate_delete(self.deck_item_route, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_204)

    def test_delete_deck_not_exists(self):
        self.simulate_delete(self.deck_item_route_not_exists, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_404)


class DeckItemShuffleTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(DeckItemShuffleTestCase, self).setUp()
        body = self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.deck_id = body['id']
        self.deck_item_shuffle_route = '{0}/{1}/shuffle'.format(DECK_COLLECTION_ROUTE, self.deck_id)
        self.deck_item_shuffle_route_not_exists = '{0}/9999999/shuffle'.format(DECK_COLLECTION_ROUTE)

    def test_shuffle_deck(self):
        body = self.simulate_post(self.deck_item_shuffle_route, {}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['id'], self.deck_id)
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

    def test_shuffle_deck_not_exists(self):
        self.simulate_post(self.deck_item_shuffle_route_not_exists, {}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_404)
