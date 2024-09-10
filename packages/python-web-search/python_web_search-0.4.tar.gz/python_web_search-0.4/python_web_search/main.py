import webbrowser
import sys
import importlib.metadata

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
    elif '-v' in sys.argv or '--version' in sys.argv:
        version()
    elif '-yt' in sys.arv or '--youtube' in sys.argv:
        youtube_search()
    elif '-r' in sys.argv or '--reddit' in sys.argv:
        reddit_search()
    else:
        google_search()


def google_search():
    search_string = "+".join(sys.argv[1:])
    url = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def youtube_search():
    search_string = "+".join(sys.argv[1:])
    url = 'https://www.youtube.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def reddit_search():
    search_string = "+".join(sys.argv[1:])
    url = 'https://www.reddit.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def help():
    print('Template: search [-h|v|yt]')
    print('options:')
    print('-h    --help      Print this Help.')
    print('-v    --version   Print software version and exit.')
    print('-yt   --youtube   Search youtube instead')
    print('-r    --reddit    Search reddit instead')


def version():
    print('python_web_search', importlib.metadata.version('python_web_search'))


if __name__ == '__main__':
    main()