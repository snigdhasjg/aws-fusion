from aws_console.input_output.cli import parse_arguments
from aws_console.input_output.browser import open_console

from aws_console.credentials import aws_credentials
from aws_console.aws_console_login import signin_url

def main():
    args = parse_arguments()

    creds, region_name = aws_credentials(args)
    url = signin_url(creds, region_name)
    
    open_console(url, args)

if __name__ == '__main__':
    main()
