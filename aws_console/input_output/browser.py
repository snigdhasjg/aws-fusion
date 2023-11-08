import webbrowser
import pyperclip
import sys

def open_console(url: str, copy_to_clipboard, print_output):
    if copy_to_clipboard:
        pyperclip.copy(url)
    elif print_output:
        print(url)
    elif not webbrowser.open_new_tab(url):
        sys.exit("No browser found. Try --help for other options")