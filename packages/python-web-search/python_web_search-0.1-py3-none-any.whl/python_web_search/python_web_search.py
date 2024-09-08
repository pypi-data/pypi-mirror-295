import webbrowser

def convert(s):  
    str1 = "+"  
    return(str1.join(s))  

def search():
    search_string = input('What to search: ')

    search = 'https://www.google.com/search?q=' + search_string
    webbrowser.open_new_tab(search)

def hello_world():
    print('hello world')