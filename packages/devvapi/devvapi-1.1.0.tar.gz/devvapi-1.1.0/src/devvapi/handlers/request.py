from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
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
            self.wfile.write(b"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Swagger UI</title>
                    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
                </head>
                <body>
                    <div id="swagger-ui"></div>
                    <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
                    <script>
                        window.onload = function() {
                            const ui = SwaggerUIBundle({
                                url: '/swagger.json',
                                dom_id: '#swagger-ui',
                            });
                        };
                    </script>
                </body>
                </html>
            """)
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
