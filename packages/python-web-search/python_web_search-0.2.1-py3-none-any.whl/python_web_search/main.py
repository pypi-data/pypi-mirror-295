import webbrowser

def search():
    search_string = input('What to search: ').replace(' ', '+')
    url = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    search()