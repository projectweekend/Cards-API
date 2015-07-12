import falcon
from psycopg2 import IntegrityError
from app.utils.misc import make_code


class DeckCollection(object):

    def on_post(self, req, res):
        req.context['result'] = {
            'code': make_code()
        }
        res.status = falcon.HTTP_CREATED
