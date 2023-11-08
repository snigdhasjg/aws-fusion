from .input_output.cli import open_console_arguments, credential_process_arguments
from .input_output.browser import open_console

from .aws_session_credential import aws_session_credential
from .aws_login_api import signin_url
from .system_credential_store import store_aws_credential, get_aws_credential

__version__ = '0.4'


def aws_console():
    args = open_console_arguments()

    __show_version_if_requested(args)

    creds, region_name = aws_session_credential(args.profile, args.region)
    url = signin_url(creds, region_name)

    open_console(url, args.clip, args.stdout)


def aws_system_credential():
    args = credential_process_arguments()

    __show_version_if_requested(args)

    if args.command == 'store':
        store_aws_credential(args.account_id, args.username, args.access_key, args.secret_key)
    elif args.command == 'get':
        get_aws_credential(args.account_id, args.username, args.access_key, args.credential_process)


def __show_version_if_requested(args):
    if args.version:
        print(__version__)
        return
