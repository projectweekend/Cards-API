from urlparse import urlparse
import falcon
from cerberus import Validator


class CustomValidator(Validator):

    def _validate_url_or_blank(self, url_or_blank, field, value):
        if url_or_blank and value != '':
            parsed = urlparse(value)
            valid_scheme = parsed.scheme in ['http', 'https']
            valid_netloc = parsed.netloc != ''
            valid_path = parsed.path != ''
            if not valid_scheme or not valid_netloc or not valid_path:
                self._error(field, 'Must be a valid URL')


class BaseValidationMixin(object):

    def _validate_request(self, validator, request_data):
        if not validator.validate(request_data):
            raise falcon.HTTPBadRequest('Bad request', validator.errors)

    def validate_post(self, request_data):
        self._validate_request(CustomValidator(self.schema_for_post), request_data)

    def validate_put(self, request_data):
        self._validate_request(CustomValidator(self.schema_for_put), request_data)
