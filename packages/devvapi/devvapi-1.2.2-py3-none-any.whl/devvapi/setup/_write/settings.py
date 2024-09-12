import string
import random
import requests

def _type(project_name: str):
    file_url = 'https://raw.githubusercontent.com/sk1llpy/devvapi/prouction/src/devvapi/setup/default/conf/settings.py'
    file = requests.get(url=file_url) 

    if file.status_code == 200:
        code = file.text

        symbols = [letter for letter in string.ascii_letters]
        symbols.extend([
            symbol for symbol in string.punctuation.replace("'", "a").replace('"', "A")
        ])
        
        symbols.extend([str(number) for number in range(0,10)])

        get_secret_key = lambda: "".join([random.choices(symbols)[-1] for count in range(0, 50)])

        code = code.replace("(___random__secret__key___)", get_secret_key())
        code = code.replace("(___project__name___)", project_name)
    
        with open(f'{project_name}/conf/settings.py', 'w') as file:
            file.write(code)