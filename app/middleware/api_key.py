import falcon
from app.config import API_KEY


class APIKey(object):

    def process_request(self, req, res):
        req.context['api_key'] = req.get_header('X-API-Key')
        if req.context['api_key'] != API_KEY:
            title = 'Unauthorized'
            description = 'Invalid API Key'
            raise falcon.HTTPUnauthorized(title, description)
