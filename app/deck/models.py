import json
from pycards import Deck
from pycards import StandardPlayingCard
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


class Card(StandardPlayingCard):

    def __init__(self, rank, suit, back_image, front_image):
        super(Card, self).__init__(rank=rank, suit=suit)
        self.back_image = back_image
        self.front_image = front_image

    @classmethod
    def generate_cards(cls, config=DEFAULT_CARDS_CONFIG):
        for card in config['cards']:
            rank, suit = card.split('_')
            back_image = '{0}/back.png'.format(config['image_path'])
            front_image = '{0}/{1}-{2}.png'.format(config['image_path'], rank, suit)
            yield cls(rank=rank, suit=suit, back_image=back_image, front_image=front_image)


class DeckOfCards(object):

    def __init__(self, id, api_key, deck):
        self.id = id
        self.api_key = api_key
        self.deck = deck

    def shuffle(self):
        self.deck.shuffle()

    def save(self, cursor):
        if self.id is None:
            sql_params = [self.api_key, self.deck.to_json(), ]
            cursor.callproc('sp_app_decks_insert', sql_params)
            result = cursor.fetchone()
            self.id = result[0]['id']
        else:
            sql_params = [self.api_key, self.id, self.deck.to_json(), ]
            cursor.callproc('sp_app_decks_update', sql_params)

    def to_dict(self):
        output = {}
        for k, v in self.__dict__.items():
            if k == 'deck':
                output['cards_remaining'] = v.cards_remaining
                output['cards_removed'] = v.cards_removed
            else:
                output[k] = v
        return output

    @classmethod
    def create(cls, api_key, count=1):
        deck = Deck.generate_deck(card_cls=Card, count=count)
        return cls(id=None, api_key=api_key, deck=deck)
