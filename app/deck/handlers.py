import falcon
from app.utils.hooks import api_key_required
from app.deck.validation import DeckValidationMixin
from app.deck.data import DataManagerMixin


@falcon.before(api_key_required)
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


@falcon.before(api_key_required)
class DeckItem(DeckValidationMixin, DataManagerMixin):

    def on_get(self, req, res, deck_id):
        api_key = req.context['api_key']
        req.context['result'] = self.get_deck(api_key, deck_id)
        res.status = falcon.HTTP_OK if req.context['result'] else falcon.HTTP_NOT_FOUND
