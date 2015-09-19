import json
from pycards import BaseDeck
from pycards import PlayingCardWithImages
from app.config import CARD_IMAGE_PATH


DEFAULT_CARDS_CONFIG = {
    'cards': (
        'ACE_SPADES', '2_SPADES', '3_SPADES', '4_SPADES', '5_SPADES', '6_SPADES', '7_SPADES', '8_SPADES', '9_SPADES', '10_SPADES', 'JACK_SPADES', 'QUEEN_SPADES', 'KING_SPADES',
        'ACE_DIAMONDS', '2_DIAMONDS', '3_DIAMONDS', '4_DIAMONDS', '5_DIAMONDS', '6_DIAMONDS', '7_DIAMONDS', '8_DIAMONDS', '9_DIAMONDS', '10_DIAMONDS', 'JACK_DIAMONDS', 'QUEEN_DIAMONDS', 'KING_DIAMONDS',
        'ACE_CLUBS', '2_CLUBS', '3_CLUBS', '4_CLUBS', '5_CLUBS', '6_CLUBS', '7_CLUBS', '8_CLUBS', '9_CLUBS', '10_CLUBS', 'JACK_CLUBS', 'QUEEN_CLUBS', 'KING_CLUBS',
        'ACE_HEARTS', '2_HEARTS', '3_HEARTS', '4_HEARTS', '5_HEARTS', '6_HEARTS', '7_HEARTS', '8_HEARTS', '9_HEARTS', '10_HEARTS', 'JACK_HEARTS', 'QUEEN_HEARTS', 'KING_HEARTS',
    ),
    'image_path': CARD_IMAGE_PATH
}


class DeckOfCards(object):

    def __init__(self, api_key, id=None, deck=None, count=1):
        cards = list(PlayingCardWithImages.generate_cards(config=DEFAULT_CARDS_CONFIG))
        self.id = id
        self.api_key = api_key
        if deck is None:
            self.deck = BaseDeck(cards=cards, count=count)
        else:
            self.deck = deck

    def save(self, cursor):
        deck_json = self.deck.to_json()
        if self.id is None:
            cursor.callproc('sp_app_deck_insert', [self.api_key, deck_json, ])
            result = cursor.fetchone()
            self.id = result[0]['id']
        else:
            cursor.callproc('sp_app_deck_update', [self.id, self.api_key, deck_json, ])

    def delete(self, cursor):
        cursor.callproc('sp_app_deck_delete', [self.id, self.api_key, ])
        result = cursor.fetchone()
        if not result:
            # raise a not found exception
            pass

    @classmethod
    def get_list(cls, cursor, api_key):
        cursor.callproc('sp_app_deck_list', [api_key, ])
        result = cursor.fetchone()
        for item in result:
            pass

    @classmethod
    def get_one(cls, cursor, api_key, id):
        cursor.callproc('sp_app_deck_select', [id, api_key, ])
        result = cursor.fetchone()
        if not result:
            # raise a not found exception
            pass
        result = result[0]
        # Need to be able to create a deck specifying cards remaining and removed instead of just cards
        # generate list of cards from json
        # return cls passing in the cards
