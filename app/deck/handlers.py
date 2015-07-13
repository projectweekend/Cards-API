import falcon
from app.utils.hooks import api_key_required
from app.deck.validation import DeckValidationMixin
from app.deck.data import DeckManagerMixin, DataManagerMixin


@falcon.before(api_key_required)
class DeckCollection(DeckValidationMixin, DeckManagerMixin, DataManagerMixin):

    def on_post(self, req, res):
        api_key = req.context['api_key']
        count = req.context['data']['count']
        new_deck = self.new_deck(count)
        req.context['result'] = self.add_deck(api_key, new_deck)
        res.status = falcon.HTTP_CREATED
