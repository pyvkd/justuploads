from wsgiref import simple_server
from main import app
if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8090, app)
    httpd.serve_forever()
