import json
import falcon


class JSONBodyParser(object):

    def process_request(self, req, res):
        if req.content_type != 'application/json':
            message = "Content type must be 'application/json'"
            raise falcon.HTTPBadRequest('Bad request', message)
        data = req.stream.read()
        if data:
            try:
                req.context['data'] = json.loads(data)
            except ValueError:
                message = "Request body is not valid JSON"
                raise falcon.HTTPBadRequest('Bad request', message)
