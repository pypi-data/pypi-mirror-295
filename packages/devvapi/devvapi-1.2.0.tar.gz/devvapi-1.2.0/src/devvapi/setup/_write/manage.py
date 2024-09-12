import requests

def _type(project_name: str):
    manage_file__url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/manage.py'
    manage__file = requests.get(manage_file__url)

    if manage__file.status_code == 200:
        manage__file = manage__file.text
        
        with open(f'{project_name}/manage.py', 'w') as manage_file:
            manage_file.write(manage__file)
