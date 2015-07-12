import falcon
from psycopg2 import IntegrityError
from app.utils.misc import make_code
from app.utils.hooks import api_key_required
from app.deck.validation import DeckValidationMixin


@falcon.before(api_key_required)
class DeckCollection(DeckValidationMixin):

    def on_post(self, req, res):
        # TODO: add to database
        res.status = falcon.HTTP_CREATED
