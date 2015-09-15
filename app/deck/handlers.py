import falcon
from app.deck.mixins import ValidationMixin
from app.deck.models import DeckOfCards


class DeckCollection(ValidationMixin):

    def on_post(self, req, res):
        count = req.context['data']['count']
        api_key = req.context['api_key']

        deck = DeckOfCards(api_key=api_key, count=count)
        deck.save()

        req.context['result'] = {
            'id': deck.id,
            'remaining': deck.cards_remaining,
            'removed': deck.cards_removed
        }
        res.status = falcon.HTTP_201
