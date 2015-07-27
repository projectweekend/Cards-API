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
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

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

    def test_list_decks(self):
        self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_CREATED)

        body = self.simulate_get(DECK_COLLECTION_ROUTE, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertEqual(len(body), 1)
        self.assertIn('id', body[0].keys())
        self.assertEqual(body[0]['remaining'], 52)
        self.assertEqual(body[0]['removed'], 0)


class DeckItemTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(DeckItemTestCase, self).setUp()
        body = self.simulate_post(
            DECK_COLLECTION_ROUTE,
            VALID_DATA,
            api_key=self.api_key)
        self.deck_item_route = '{0}/{1}'.format(DECK_COLLECTION_ROUTE, body['id'])
        self.deck_item_route_not_exists = '{0}/999999'.format(DECK_COLLECTION_ROUTE)

    def test_get_deck_by_id(self):
        body = self.simulate_get(self.deck_item_route, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertIn('id', body.keys())
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

    def test_get_deck_by_id_not_exists(self):
        self.simulate_get(self.deck_item_route_not_exists, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_NOT_FOUND)


class DeckItemShuffleTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(DeckItemShuffleTestCase, self).setUp()
        body = self.simulate_post(
            DECK_COLLECTION_ROUTE,
            VALID_DATA,
            api_key=self.api_key)
        self.deck_item_shuffle_route = '{0}/{1}/shuffle'.format(DECK_COLLECTION_ROUTE, body['id'])
        self.deck_item_shuffle_route_not_exists = '{0}/999999/shuffle'.format(DECK_COLLECTION_ROUTE)

    def test_shuffle_deck_by_id(self):
        body = self.simulate_put(
            self.deck_item_shuffle_route,
            {'target': 'all'},
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_OK)
        self.assertIn('id', body.keys())
        self.assertEqual(body['remaining'], 52)
        self.assertEqual(body['removed'], 0)

    def test_shuffle_deck_by_id_not_exists(self):
        self.simulate_put(
            self.deck_item_shuffle_route_not_exists,
            {'target': 'all'},
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_NOT_FOUND)

    def test_shuffle_deck_with_invalid_data(self):
        body = self.simulate_put(
            self.deck_item_shuffle_route,
            {},
            api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_BAD_REQUEST)
        error_keys = body['description'].keys()
        self.assertIn('target', error_keys)
