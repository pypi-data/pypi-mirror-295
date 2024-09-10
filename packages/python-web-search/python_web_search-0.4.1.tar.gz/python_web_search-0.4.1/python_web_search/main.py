import webbrowser
import sys
import importlib.metadata

def main():
    global args
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        try:
            args.remove('-h')
            args.remove('--help')
        except ValueError:
            pass
        help()
    elif '-v' in args or '--version' in args:
        try:
            args.remove('-v')
            args.remove('--version')
        except ValueError:
            pass
        version()
    elif '-yt' in args or '--youtube' in args:
        try:
            args.remove('-yt')
            args.remove('--youtube')
        except ValueError:
            pass
        youtube_search()
    elif '-r' in args or '--reddit' in args:
        try:
            args.remove('-r')
            args.remove('--reddit')
        except ValueError:
            pass
        reddit_search()
    else:
        google_search()


def google_search():
    search_string = "+".join(args)
    url = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def youtube_search():
    search_string = "+".join(args)
    url = 'https://www.youtube.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def reddit_search():
    search_string = "+".join(args)
    url = 'https://www.reddit.com/search?q=' + search_string
    webbrowser.open_new_tab(url)


def help():
    print('Template: search [-h|v|yt|r]')
    print('options:')
    print('-h    --help      Print this Help.')
    print('-v    --version   Print software version and exit.')
    print('-yt   --youtube   Search youtube instead')
    print('-r    --reddit    Search reddit instead')


def version():
    print('python_web_search', importlib.metadata.version('python_web_search'))


if __name__ == '__main__':
    main()