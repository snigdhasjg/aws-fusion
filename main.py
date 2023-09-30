#!/usr/bin/env python3

from input_output.cli import parse_arguments
from input_output.browser import open_console

from aws_console_login.credentials import aws_credentials
from aws_console_login.aws_operations import signin_url

def main():
    args = parse_arguments()

    creds, region_name = aws_credentials(args.profile)
    url = signin_url(creds, region_name)
    
    open_console(url, args.stdout)

if __name__ == '__main__':
    main()
