import falcon
from falcon.testing import TestBase
from app import api
from app.config import API_KEY


class MiddlewareTestCase(TestBase):

    def test_body_parser_with_invalid_json(self):
        self.api = api
        self.simulate_request(
            path='/user',
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            body='not json')
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    def test_body_parser_with_invalid_content_type(self):
        self.api = api
        self.simulate_request(
            path='/user',
            method='POST',
            headers={
                'X-API-Key': API_KEY
            },
            body='not json')
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
