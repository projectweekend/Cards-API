import json
from random import shuffle


CARDS = (
    'ACE_S', '2_S', '3_S', '4_S', '5_S', '6_S', '7_S', '8_S', '9_S', '10_S', 'JACK_S', 'QUEEN_S', 'KING_S',
    'ACE_D', '2_D', '3_D', '4_D', '5_D', '6_D', '7_D', '8_D', '9_D', '10_D', 'JACK_D', 'QUEEN_D', 'KING_D',
    'ACE_C', '2_C', '3_C', '4_C', '5_C', '6_C', '7_C', '8_C', '9_C', '10_C', 'JACK_C', 'QUEEN_C', 'KING_C',
    'ACE_H', '2_H', '3_H', '4_H', '5_H', '6_H', '7_H', '8_H', '9_H', '10_H', 'JACK_H', 'QUEEN_H', 'KING_H',
)

SUITS = {
    'S': 'SPADES',
    'D': 'DIAMONDS',
    'C': 'CLUBS',
    'H': 'HEARTS'
}


class DataManagerMixin(object):

    @staticmethod
    def _build_card(card):
        rank, s = card.split('_')
        suit = SUITS[s]
        front_image = '/path/to/front/{0}-{1}.png'.format(rank, suit)
        back_image = '/path/to/back.png'
        return {
            'rank': rank,
            'suit': SUITS[s],
            'front': front_image,
            'back': back_image
        }

    @staticmethod
    def _serialize_deck_result(database_result):
        return {
            'id': database_result['id'],
            'remaining': len(database_result['cards']['available']),
            'removed': len(database_result['cards']['removed'])
        }

    def add_deck(self, api_key, num_of_decks):
        cards = [self._build_card(c) for c in CARDS] * num_of_decks
        shuffle(cards)
        deck = json.dumps({
            'cards': {
                'available': cards,
                'removed': []
            },
            'groups': {}
        })
        self.cursor.callproc('sp_app_deck_insert', [api_key, deck, ])
        result = self.cursor.fetchone()
        return self._serialize_deck_result(result[0])

    def list_decks(self, api_key):
        self.cursor.callproc('sp_app_deck_list', [api_key, ])
        result = self.cursor.fetchone()
        return [self._serialize_deck_result(d) for d in result[0]]
