import webbrowser

def open_console(url: str, echo_to_stdout: bool):

    if echo_to_stdout:
        print(url)
    else:
        webbrowser.open(url)