from app.utils.validation import BaseValidationMixin


class DeckValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'count': {
            'type': 'integer',
            'required': True
        }
    }


class DeckShuffleValidationMixin(BaseValidationMixin):

    schema_for_put = {
        'target': {
            'type': 'string',
            'required': True
        }
    }


class DeckDrawValidationMixin(BaseValidationMixin):

    schema_for_put = {
        'count': {
            'type': 'integer',
            'required': True,
            'min': 1
        }
    }
