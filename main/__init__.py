import falcon
# from main.settings import DB as db
# from main.helpers import QueryParser
import json
import urlparse
from werkzeug.http import parse_options_header
from werkzeug.formparser import parse_form_data
from cStringIO import StringIO
from werkzeug.wsgi import LimitedStream
from werkzeug import secure_filename


class CreateTemplateExclusiveImage:
    """End point for creating dealtype"""
    def on_get(self, req, resp, stream, form={}, files={}):
        """return status 405. asks to use post api.
        """
        resp.content_type = "application/json"
        resp_dict = {"status": "error",
                     "summary": "use post request for logout"}
        resp.body = (json.dumps(resp_dict))

    def on_post(self, req, resp, stream, form={}, files={}):
        """
        """
        file = files.get('file', [''])[0]
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
        resp.status = falcon.HTTP_200
        resp.content_type = "application/json"
        resp_dict = {"status": "success",
                     "summary": "File uploaded"}
        resp.body = (json.dumps(resp_dict))


def generate_formdata(req, resp, params):
    """sets params['form'], params['files'], params['stream']
    to pass to every endpoint.
    """
    if req.method != 'GET':
        mimetype, options = parse_options_header(req.get_header('content-type'))
        data = req.stream.read()
        environ = {'wsgi.input': StringIO(data),
                   'CONTENT_LENGTH': str(len(data)),
                   'CONTENT_TYPE': '%s; boundary=%s' %
                   (mimetype, options['boundary']),
                   'REQUEST_METHOD': 'POST'}
        stream, form, files = parse_form_data(environ)
        params['stream'], params['form'], params['files'] = stream, dict(form),\
            dict(files)
        return True
    else:
        di = urlparse.parse_qsl(req.query_string)
        params['form'] = dict(di)
        params['stream'] = LimitedStream()
        params['files'] = dict()
    return True

# hooks to be executed on every request before reaching to the endpoint
app = falcon.API(before=[generate_formdata])

# importing all the endpoints
cr = CreateTemplateExclusiveImage()

app.add_route('/upload', cr)
