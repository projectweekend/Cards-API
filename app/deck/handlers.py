import falcon
from pycards import BaseDeck, PlayingCardWithImages
from pycards.errors import NoCardsRemaining
from app.config import DEFAULT_CARDS_CONFIG
from app.deck.mixins import (
    CollectionValidationMixin,
    ShuffleValidationMixin,
    DrawValidationMixin)


def to_response_dict(id, deck):
        return {
            'id': id,
            'remaining': deck.cards_remaining,
            'removed': deck.cards_removed
        }


class DeckCollection(CollectionValidationMixin):

    def on_post(self, req, res):
        count = req.context['data']['count']
        api_key = req.context['api_key']

        cards = list(PlayingCardWithImages.generate_cards(config=DEFAULT_CARDS_CONFIG))
        deck = BaseDeck(cards=cards, count=count)
        deck.shuffle()

        sql_params = [api_key, deck.to_json()]
        self.cursor.callproc('sp_app_deck_insert', sql_params)
        result = self.cursor.fetchone()

        req.context['result'] = to_response_dict(id=result[0]['id'], deck=deck)
        res.status = falcon.HTTP_201

    def on_get(self, req, res):
        api_key = req.context['api_key']

        self.cursor.callproc('sp_app_deck_list', [api_key, ])
        result = self.cursor.fetchone()

        req.context['result'] = []
        for r in result[1]:
            deck = BaseDeck.from_dict(card_cls=PlayingCardWithImages, deck_dict=r['deck'])
            req.context['result'].append(to_response_dict(id=r['id'], deck=deck))
        res.status = falcon.HTTP_200


class DeckItem(object):

    def on_get(self, req, res, deck_id):
        api_key = req.context['api_key']

        self.cursor.callproc('sp_app_deck_select', [deck_id, api_key, ])
        result = self.cursor.fetchone()
        if not result:
            raise falcon.HTTPNotFound

        deck = BaseDeck.from_dict(card_cls=PlayingCardWithImages, deck_dict=result[0]['deck'])
        req.context['result'] = to_response_dict(id=result[0]['id'], deck=deck)
        res.status = falcon.HTTP_200

    def on_delete(self, req, res, deck_id):
        api_key = req.context['api_key']

        self.cursor.callproc('sp_app_deck_delete', [deck_id, api_key, ])
        result = self.cursor.fetchone()
        if not result[0]:
            raise falcon.HTTPNotFound
        res.status = falcon.HTTP_204


class DeckItemShuffle(ShuffleValidationMixin):

    def on_post(self, req, res, deck_id):
        api_key = req.context['api_key']

        self.cursor.callproc('sp_app_deck_select', [deck_id, api_key, ])
        result = self.cursor.fetchone()
        if not result:
            raise falcon.HTTPNotFound

        deck = BaseDeck.from_dict(card_cls=PlayingCardWithImages, deck_dict=result[0]['deck'])
        deck.shuffle()

        self.cursor.callproc('sp_app_deck_update', [deck_id, api_key, deck.to_json(), ])
        req.context['result'] = to_response_dict(id=result[0]['id'], deck=deck)
        res.status = falcon.HTTP_200


class DeckItemDraw(DrawValidationMixin):

    def on_post(self, req, res, deck_id):
        api_key = req.context['api_key']
        count = req.context['data']['count']

        self.cursor.callproc('sp_app_deck_select', [deck_id, api_key, ])
        result = self.cursor.fetchone()
        if not result:
            raise falcon.HTTPNotFound

        deck = BaseDeck.from_dict(card_cls=PlayingCardWithImages, deck_dict=result[0]['deck'])
        try:
            cards = [deck.draw_card() for _ in range(count)]
        except NoCardsRemaining:
            raise falcon.HTTPConflict(title='Conflict', description='Deck is empty')

        self.cursor.callproc('sp_app_deck_update', [deck_id, api_key, deck.to_json(), ])

        req.context['result'] = {
            'deck': to_response_dict(id=result[0]['id'], deck=deck),
            'cards': [card.to_dict() for card in cards]
        }
        res.status = falcon.HTTP_200
