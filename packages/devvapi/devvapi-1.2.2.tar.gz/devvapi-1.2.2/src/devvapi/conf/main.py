import inspect
import json
from ..apps.core import App, AppConfig


class DevvAPI:
    def __init__(self):
        self.router = App(AppConfig())
        self.routers = []
        self.docs_url = "/docs"
        self.swagger_docs = {
            "openapi": "3.0.0",
            "info": {
                "title": "Devv API",
                "version": "1.0.0"
            },
            "paths": {}
        }

    def include_router(self, router):
        self.routers.append(router)
        self._merge_router_to_swagger(router)

    def _merge_router_to_swagger(self, router):
        for path_pattern, methods in router.get_routes().items():
            for method, route_info in methods.items():
                path = route_info["path"]

                if path not in self.swagger_docs["paths"]:
                    self.swagger_docs["paths"][path] = {}

                self.swagger_docs["paths"][path][method.lower()] = {
                    "summary": route_info["description"],
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }

    def add_route(self, path, method, handler, description=""):
        self.router.add_route(path, method, handler, description)
        if path not in self.swagger_docs["paths"]:
            self.swagger_docs["paths"][path] = {}
        self.swagger_docs["paths"][path][method.lower()] = {
            "summary": description,
            "responses": {
                "200": {
                    "description": "Successful response"
                }
            }
        }

    def get(self, path, description=""):
        return self.route(path, 'GET', description)

    def post(self, path, description=""):
        return self.route(path, 'POST', description)

    def route(self, path, method, description=""):
        def decorator(handler):
            self.add_route(path, method, handler, description)
            return handler
        return decorator

    async def handle_request(self, handler, request_handler, path_params):
        try:
            if inspect.iscoroutinefunction(handler):
                response = await handler(request_handler, **path_params)
            else:
                response = handler(request_handler, **path_params)

            if isinstance(response, str):
                request_handler.send_response(200)
                request_handler.send_header('Content-type', 'text/html')
                request_handler.end_headers()
                request_handler.wfile.write(response.encode())
            elif isinstance(response, dict):
                request_handler.send_response(200)
                request_handler.send_header('Content-type', 'application/json')
                request_handler.end_headers()
                request_handler.wfile.write(json.dumps(response).encode())
            else:
                request_handler.send_response(500)
                request_handler.send_header('Content-type', 'text/html')
                request_handler.end_headers()
                request_handler.wfile.write(b"Internal Server Error: Unsupported response type")
        except Exception as e:
            request_handler.send_response(500)
            request_handler.send_header('Content-type', 'text/html')
            request_handler.end_headers()
            request_handler.wfile.write(f"Internal Server Error: {e}".encode())

    def find_handler(self, method, path):
        handler, path_params = self.router.find_handler(method, path)
        if handler:
            return handler, path_params
        for router in self.routers:
            handler, path_params = router.find_handler(method, path)
            if handler:
                return handler, path_params
        return None, None

    def get_swagger_json(self):
        return self.swagger_docs
