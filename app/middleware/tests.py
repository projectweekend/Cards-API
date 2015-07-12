import falcon
from falcon.testing import TestBase
from app import api


class MiddlewareTestCase(TestBase):

    def test_body_parser_with_invalid_json(self):
        self.api = api
        self.simulate_request(
            path='/user',
            method='POST',
            headers={'Content-Type': 'application/json'},
            body='not json')
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    def test_body_parser_with_invalid_content_type(self):
        self.api = api
        self.simulate_request(
            path='/user',
            method='POST',
            body='not json')
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
