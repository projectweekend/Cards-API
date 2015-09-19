import falcon
from app.deck.mixins import ValidationMixin
from app.deck.models import DeckOfCards


class DeckCollection(ValidationMixin):

    def on_post(self, req, res):
        count = req.context['data']['count']
        api_key = req.context['api_key']

        deck_of_cards = DeckOfCards(api_key=api_key, count=count)
        deck_of_cards.save(cursor=self.cursor)

        req.context['result'] = deck_of_cards.to_response_dict()
        res.status = falcon.HTTP_201

    def on_get(self, req, res):
        pass
