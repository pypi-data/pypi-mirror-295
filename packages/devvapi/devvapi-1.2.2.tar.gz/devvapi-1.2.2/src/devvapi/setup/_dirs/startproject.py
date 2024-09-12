import os

def _create(project_name: str):
    directories = [
        project_name,
        os.path.join(project_name, 'conf'),
        os.path.join(project_name, 'src'),
        os.path.join(project_name, 'src', 'v1'),
    ]

    files = [
        os.path.join(project_name, 'manage.py'),

        os.path.join(project_name, 'conf', '__init__.py'),
        os.path.join(project_name, 'conf', 'settings.py'),
        os.path.join(project_name, 'conf', 'apps.py'),

        os.path.join(project_name, 'src', '__init__.py'),
        os.path.join(project_name, 'src', 'v1', '__init__.py'),
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write("")