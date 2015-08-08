import falcon
from app.deck.validation import (
    DeckValidationMixin,
    DeckShuffleValidationMixin,
    DeckDrawValidationMixin)
from app.deck.data import DataManagerMixin


class DeckCollection(DeckValidationMixin, DataManagerMixin):

    def on_post(self, req, res):
        api_key = req.context['api_key']
        count = req.context['data']['count']
        req.context['result'] = self.add_deck(api_key, count)
        res.status = falcon.HTTP_CREATED

    def on_get(self, req, res):
        api_key = req.context['api_key']
        req.context['result'] = self.list_decks(api_key)
        res.status = falcon.HTTP_OK


class DeckItem(DeckValidationMixin, DataManagerMixin):

    def on_get(self, req, res, deck_id):
        api_key = req.context['api_key']
        req.context['result'] = self.get_deck(api_key, deck_id)
        res.status = falcon.HTTP_OK if req.context['result'] else falcon.HTTP_NOT_FOUND


class DeckItemShuffle(DeckShuffleValidationMixin, DataManagerMixin):

    def on_put(self, req, res, deck_id):
        api_key = req.context['api_key']
        target = req.context['data']['target']
        req.context['result'] = self.shuffle_deck(api_key, deck_id, target)
        res.status = falcon.HTTP_OK if req.context['result'] else falcon.HTTP_NOT_FOUND


class DeckItemDraw(DeckDrawValidationMixin, DataManagerMixin):

    def on_put(self, req, res, deck_id):
        api_key = req.context['api_key']
        number_of_cards = req.context['data']['count']
        req.context['result'] = self.draw_cards_from_deck(api_key, deck_id, number_of_cards)
        res.status = falcon.HTTP_OK if req.context['result'] else falcon.HTTP_NOT_FOUND
