import webbrowser

def open_console(url: str, argument):
    if argument.stdout:
        print(url)
    else:
        webbrowser.open(url)