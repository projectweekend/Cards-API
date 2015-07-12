from app.utils.validation import BaseValidationMixin


class DeckValidationMixin(BaseValidationMixin):

    schema_for_post = {
        'count': {
            'type': 'integer',
            'required': True
        }
    }
