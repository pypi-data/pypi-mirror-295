import webbrowser

def search():
    search_string = "+".join(input('What to search: '))
    url = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(url)
