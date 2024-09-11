def _type(project_name: str, version: int, app_name: str):
    with open('/home/skilldev/Desktop/devvapi/setup/default/app/app.py', 'r') as app__file:
        app__file = app__file.read()

        app__file = app__file.replace("___AppName___", app_name.capitalize())
        app__file = app__file.replace("(___app_name___)", app_name)
        app__file = app__file.replace('"(___version___)"', str(version))

        with open(f'{project_name}/src/v{version}/{app_name}/app.py', 'w') as app_file:
            app_file.write(app__file)

    with open('/home/skilldev/Desktop/devvapi/setup/default/app/views.py', 'r') as views__file:
        views__file = views__file.read()
        
    with open(f'{project_name}/src/v{version}/{app_name}/views.py', 'w') as views_file:
        views_file.write(views__file)