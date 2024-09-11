def _type(project_name: str):
    with open(f'{project_name}/devvapi.py', 'w') as lib:
        with open('/home/skilldev/Desktop/devvapi/devvapi.py', 'r') as main:
            main_source = main.read()
            lib.write(main_source)