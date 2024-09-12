import sys

def main():
    try:
        from devvapi.core.management import execute_command
    except ImportError as exc:
        raise exc

    execute_command(sys.argv)

if __name__ == '__main__':
    main()