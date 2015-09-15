import falcon
from cerberus import Validator


DECK_CREATE_SCHEMA = {
    'count': {
        'type': 'integer'
    }
}


class ValidationMixin(object):

    def validate_post(self, data):
        v = Validator(DECK_CREATE_SCHEMA)
        if not v.validate(data):
            raise falcon.HTTPBadRequest(
                title='Bad Request',
                description=v.errors)
