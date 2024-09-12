import requests

def _type(project_name: str):
    file_url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/conf/apps.py'
    file = requests.get(file_url)

    if file.status_code == 200:
        code = file.text

        with open(f'{project_name}/conf/apps.py', 'w') as file:
            file.write(code)