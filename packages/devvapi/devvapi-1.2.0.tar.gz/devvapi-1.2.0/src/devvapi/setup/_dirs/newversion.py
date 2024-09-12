import os

def _create(version_path):
    directories = [
        version_path,
    ]
    
    files = [
        os.path.join(version_path, '__init__.py'),
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write("")
