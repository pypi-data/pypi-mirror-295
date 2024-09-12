from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import requests
import asyncio

from ..conf.main import DevvAPI


class RequestHandler(BaseHTTPRequestHandler):
    api: DevvAPI = None

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/swagger.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.api.get_swagger_json()).encode())
        elif parsed_path.path == self.api.docs_url:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            swagger_html__url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/swagger/index.html'
            swagger__html = requests.get(url=swagger_html__url)

            try:
                self.wfile.write(swagger__html.text.encode('utf-8'))
            except:
                self.wfile.write(b"""<h1>Error on Swagger!</h1>""")
        else:
            handler, path_params = self.api.find_handler('GET', parsed_path.path)
            if handler:
                asyncio.run(self.api.handle_request(handler, self, path_params))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'404 Not Found')

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        handler, path_params = self.api.find_handler('POST', parsed_path.path)
        if handler:
            asyncio.run(self.api.handle_request(handler, self, path_params))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
