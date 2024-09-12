import time
import datetime
from http.server import HTTPServer

from ..apps.core import App
from ..conf.main import DevvAPI
from ..handlers.request import RequestHandler

def run():
    import os

    application = DevvAPI()

    with open('conf/settings.py', 'r') as settings:
        settings_context = {}
        settings_source = exec(settings.read().encode('utf-8'), settings_context)

        application.docs_url = settings_context['DOCS_URL']
    
    with open('conf/apps.py', 'r') as apps:
        apps_context = {}
        apps_source = exec(apps.read().encode('utf-8'), apps_context)

    apps_instance: list[App] = []
    for installed_app in apps_context.get('INSTALLED_APPS'):
        version, app_name = installed_app.split('.')

        version_path = os.path.join('src', version)

        if os.path.exists(version_path):
            app_path = os.path.join('src', version, app_name, 'app.py')
            app_views_path = os.path.join('src', version, app_name, 'views.py')

            if os.path.exists(app_path):
                with open(app_path, 'r') as app_ins:
                    app_code = app_ins.read()
                    app_context = {}

                    with open(app_views_path, 'r') as views_file:
                        app_code += "\n\n"
                        app_code += (views_file.read()).replace(
                            "from .app import app", f"from src.{version}.{app_name}.app import app"
                        )

                    app_source = exec(app_code.encode('utf-8'), app_context)

                    if 'app' in app_context:
                        if isinstance(app_context['app'], App):
                            apps_instance.append(app_context['app'])

    for app in apps_instance:
        application.include_router(app)

    server_address = (settings_context['HOST'].split(':')[0], int(settings_context['HOST'].split(':')[-1]))
    RequestHandler.api = application
    httpd = HTTPServer(server_address, RequestHandler)

    current_time = datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    messages = [
        "Watching for file changes with StatReloader",
        "Performing system checks...",
        "",
        current_time,
        f"Project: {settings_context.get('PROJECT_NAME')}",
        f"DevvAPI, using settings 'conf.settings'",
        f"Starting development server at http://{settings_context['HOST']}",
        "Quit the server with CONTROL-C."
    ]
    
    for message in messages:
        print(message)
        time.sleep(0.01)

    httpd.serve_forever()

