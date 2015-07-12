class RequestValidation(object):

    def process_resource(self, req, res, resource):
        if req.method == 'POST':
            resource.validate_post(req.context['data'])
        if req.method == 'PUT':
            resource.validate_put(req.context['data'])
