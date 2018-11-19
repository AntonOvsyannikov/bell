#!/usr/bin/env python
import traceback
from importlib import reload

HOST = '0.0.0.0'
PORT = 8000

from http.server import BaseHTTPRequestHandler, HTTPServer
# noinspection PyUnresolvedReferences
import graph


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            global graph
            graph = reload(graph)
            status, contenttype, content = graph.result()

        except Exception:
            # status, contenttype, content = 500, 'text/html', '{}'.format(e)
            status, contenttype, content = 500, 'text/text', traceback.format_exc().encode("utf8")

        self.send_response(status)
        self.send_header('Content-type', contenttype)
        self.end_headers()
        self.wfile.write(content)


def run():
    print('Starting server at {}:{}'.format(HOST, PORT))
    httpd = HTTPServer((HOST, PORT), RequestHandler)
    print('Server is running...')
    httpd.serve_forever()


run()
