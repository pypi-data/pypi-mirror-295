import re

class AppConfig:
    path = None
    name = None
    version: int = 1

class App:
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.routes = {}

    def add_route(self, path, method, handler, description=""):
        full_path = f"/v{self.app_config.version}{self.app_config.path}{path}"

        path_pattern = re.sub(r'{(\w+)}', r'(?P<>[^/]+)', full_path)
        path_regex = f'^{path_pattern}/?$'

        if path_regex not in self.routes:
            self.routes[path_regex] = {}

        self.routes[path_regex][method.upper()] = {"handler": handler, "description": description, "path": full_path}

    def get(self, path, description=""):
        return self.route(path, 'GET', description)

    def post(self, path, description=""):
        return self.route(path, 'POST', description)

    def route(self, path, method, description=""):
        def decorator(handler):
            self.add_route(path, method, handler, description)
            return handler
        return decorator

    def find_handler(self, method, path):
        for path_pattern, methods in self.routes.items():
            match = re.match(path_pattern, path)
            if match:
                route_info = methods.get(method.upper(), None)
                if route_info:
                    return route_info["handler"], match.groupdict()
        return None, None

    def get_routes(self):
        return self.routes
