import json


class JSONResponse(object):

    def process_response(self, req, res, resource):
        if 'result' in req.context:
            res.body = json.dumps(req.context['result'])
        else:
            res.body = None
