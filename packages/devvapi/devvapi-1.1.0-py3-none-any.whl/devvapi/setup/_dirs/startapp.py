import os

def _create(project_name: str, version: int, app_name: str):
    version_path = os.path.join(project_name, 'src', f'v{version}')

    if not os.path.exists(version_path):
        raise FileNotFoundError(f"Version 'v{version}' not found!")

    directories = [
        os.path.join(version_path, app_name),
        os.path.join(version_path, app_name, 'db')
    ]
    
    files = [
        os.path.join(version_path, app_name, '__init__.py'),
        os.path.join(version_path, app_name, 'schemas.py'),
        os.path.join(version_path, app_name, 'app.py'),
        os.path.join(version_path, app_name, 'views.py'),
        os.path.join(version_path, app_name, 'db', '__init__.py'),
        os.path.join(version_path, app_name, 'db', 'models.py'),
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write("")
    
