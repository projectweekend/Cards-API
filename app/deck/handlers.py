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
