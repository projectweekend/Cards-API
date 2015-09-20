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


class DeckItemDrawTestCase(AuthenticatedAPITestCase):

    def setUp(self):
        super(DeckItemDrawTestCase, self).setUp()
        body = self.simulate_post(DECK_COLLECTION_ROUTE, VALID_DATA, api_key=self.api_key)
        self.deck_id = body['id']
        self.deck_item_draw_route = '{0}/{1}/draw'.format(DECK_COLLECTION_ROUTE, self.deck_id)
        self.deck_item_draw_route_not_exists = '{0}/9999999/draw'.format(DECK_COLLECTION_ROUTE)

    def test_draw_card(self):
        body = self.simulate_post(self.deck_item_draw_route, {'count': 1}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

        deck = body['deck']
        self.assertEqual(deck['id'], self.deck_id)
        self.assertEqual(deck['remaining'], 51)
        self.assertEqual(deck['removed'], 1)

        cards = body['cards']
        self.assertEqual(len(cards), 1)
        self.assertIn('rank', cards[0])
        self.assertIn('suit', cards[0])
        self.assertIn('front_image', cards[0])
        self.assertIn('back_image', cards[0])

        body = self.simulate_post(self.deck_item_draw_route, {'count': 5}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

        deck = body['deck']
        self.assertEqual(deck['id'], self.deck_id)
        self.assertEqual(deck['remaining'], 46)
        self.assertEqual(deck['removed'], 6)

        cards = body['cards']
        self.assertEqual(len(cards), 5)
        for card in cards:
            self.assertIn('rank', card)
            self.assertIn('suit', card)
            self.assertIn('front_image', card)
            self.assertIn('back_image', card)

    def test_draw_card_from_empty_deck(self):
        body = self.simulate_post(self.deck_item_draw_route, {'count': 52}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

        deck = body['deck']
        self.assertEqual(deck['id'], self.deck_id)
        self.assertEqual(deck['remaining'], 0)
        self.assertEqual(deck['removed'], 52)

        cards = body['cards']
        self.assertEqual(len(cards), 52)

        self.simulate_post(self.deck_item_draw_route, {'count': 1}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_409)

    def test_draw_card_invalid_data(self):
        self.simulate_post(self.deck_item_draw_route, {'count': 'abc'}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(self.deck_item_draw_route, {}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    def test_draw_card_deck_not_exists(self):
        self.simulate_post(self.deck_item_draw_route_not_exists, {'count': 1}, api_key=self.api_key)
        self.assertEqual(self.srmock.status, falcon.HTTP_404)
