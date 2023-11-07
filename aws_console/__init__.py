from .input_output.cli import parse_arguments
from .input_output.browser import open_console

from .credentials import aws_credentials
from .aws_console_login import signin_url

__version__ = '0.3'


def aws_console():
    args = parse_arguments()

    creds, region_name = aws_credentials(args)
    url = signin_url(creds, region_name)

    open_console(url, args)
