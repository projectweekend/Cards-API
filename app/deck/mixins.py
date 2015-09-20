import falcon
from cerberus import Validator


DECK_CREATE_SCHEMA = {
    'count': {
        'type': 'integer',
        'required': True
    }
}


DECK_DRAW_CARD_SCHEMA = {
    'count': {
        'type': 'integer',
        'min': 1,
        'required': True
    }
}


class CollectionValidationMixin(object):

    def validate_post(self, data):
        v = Validator(DECK_CREATE_SCHEMA)
        if not v.validate(data):
            raise falcon.HTTPBadRequest(
                title='Bad Request',
                description=v.errors)


class ShuffleValidationMixin(object):

    def validate_post(self, data):
        pass


class DrawValidationMixin(object):

    def validate_post(self, data):
        v = Validator(DECK_DRAW_CARD_SCHEMA)
        if not v.validate(data):
            raise falcon.HTTPBadRequest(
                title='Bad Request',
                description=v.errors)
