#!/usr/bin/env python3

import argparse
import os

import _dirs
import _write
import _write.lib
import _write.app
import _write.manage


def startproject(project_name):
    _dirs.startproject._create(project_name)

    _write.settings._type(project_name)
    _write.apps._type(project_name)
    _write.manage._type(project_name)
    _write.lib._type(project_name)


def startapp(app_name):
    project_name = input("Type project name: ").strip()
    
    if not os.path.exists(project_name):
        raise FileNotFoundError(f"Project '{project_name}' not found!")
    
    try:
        version = int(input("Type version (integer): ").strip())
    except ValueError:
        raise ValueError("Version must be an integer!")
    
    _dirs.startapp._create(
        project_name = project_name, 
        version = version, 
        app_name = app_name
    )

    _write.app._type(
        project_name=project_name,
        app_name=app_name,
        version=version
    )


def newversion(version: int):
    project_name = input("Type project name: ").strip()

    if not os.path.exists(project_name):
        raise FileNotFoundError(f"Project '{project_name}' not found!")

    version_path = os.path.join(project_name, 'src', f'v{version}')
    if os.path.exists(version_path):
        raise FileExistsError(f"Version 'v{version}' already exists!")
    
    _dirs.newversion._create(version_path)

    
def main():
    parser = argparse.ArgumentParser(description="My custom command-line tool")
    parser.add_argument('--startproject', metavar='project_name', type=str, help='Create a new project')
    parser.add_argument('--startapp', metavar='app_name', type=str, help='Create a new app')
    parser.add_argument('--newversion', metavar='version', type=int, help='Create a new version')
    
    args = parser.parse_args()
    
    if args.startproject:
        startproject(args.startproject)
    elif args.startapp:
        startapp(args.startapp)
    elif args.newversion:
        newversion(args.newversion)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

# To update code: chmod +x /home/skilldev/.local/bin/devvapi
