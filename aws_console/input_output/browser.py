import webbrowser
import pyperclip

def open_console(url: str, argument):
    if argument.clip:
        pyperclip.copy(url)
    elif argument.stdout:
        print(url)
    else:
        webbrowser.open(url)