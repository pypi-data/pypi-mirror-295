import webbrowser
import sys
import importlib.metadata

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
    elif '-v' in sys.argv or '--version' in sys.argv:
        version()
    else:
        search()


def search():
    search_string = "+".join(sys.argv[1:])
    url = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def help():
    print('Template: search [-h|v]')
    print('options:')
    print('-h    --help      Print this Help.')
    print('-v    --version   Print software version and exit.')


def version():
    print('python_web_search', importlib.metadata.version('python_web_search'))


if __name__ == '__main__':
    main()