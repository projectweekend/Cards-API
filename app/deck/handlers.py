import falcon
from app.utils.hooks import api_key_required
from app.deck.validation import DeckValidationMixin
from app.deck.data import DataManagerMixin


@falcon.before(api_key_required)
class DeckCollection(DeckValidationMixin, DataManagerMixin):

    def on_post(self, req, res):
        api_key = req.context['api_key']
        count = req.context['data']['count']
        new_deck = self.add_deck(api_key, count)
        req.context['result'] = {
            'id': new_deck['id'],
            'remaining': len(new_deck['cards']['available']),
            'removed': len(new_deck['cards']['removed']),
            'groups': {}
        }
        res.status = falcon.HTTP_CREATED
