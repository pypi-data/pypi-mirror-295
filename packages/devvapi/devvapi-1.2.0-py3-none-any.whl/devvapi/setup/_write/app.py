import requests

def _type(project_name: str, version: int, app_name: str):
    app_file__url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/app/app.py'
    app__file = requests.get(app_file__url)
    
    if app__file.status_code == 200:
        app__file = app__file.text
        app__file = app__file.replace("___AppName___", app_name.capitalize())
        app__file = app__file.replace("(___app_name___)", app_name)
        app__file = app__file.replace('"(___version___)"', str(version))

        with open(f'{project_name}/src/v{version}/{app_name}/app.py', 'w') as app_file:
            app_file.write(app__file)

    views_file__url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/app/views.py'
    views__file = requests.get(views_file__url)

    if views__file.status_code == 200:
        views__file = views__file.text
        
        with open(f'{project_name}/src/v{version}/{app_name}/views.py', 'w') as views_file:
            views_file.write(views__file)