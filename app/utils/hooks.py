import falcon


def api_key_required(req, res, resource):
    req.context['api_key'] = req.get_header('X-API-Key')
    if not req.context['api_key']:
        raise falcon.HTTPUnauthorized('Unauthorized', "Missing API Key ('X-API-Key')")
