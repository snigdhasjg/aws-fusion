import webbrowser
import pyperclip
import sys

def open_console(url: str, argument):
    if argument.clip:
        pyperclip.copy(url)
    elif argument.stdout:
        print(url)
    elif not webbrowser.open_new_tab(url):
        sys.exit("No browser found. Try --help for other options")