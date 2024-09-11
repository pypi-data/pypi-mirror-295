def _type(project_name: str):
    with open('/home/skilldev/Desktop/devvapi/setup/default/conf/apps.py', 'r') as file:
        code = file.read()

        with open(f'{project_name}/conf/apps.py', 'w') as file:
            file.write(code)