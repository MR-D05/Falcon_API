import json
import falcon


class Middleware(object):

    def process_request(self, req, resp):
        if req.content_type == 'application/json':
            data = req.stream.read().decode('UTF-8')
            try:
                req.context['d'] = json.loads(data)
            except ValueError:
                raise falcon.HTTPBadRequest