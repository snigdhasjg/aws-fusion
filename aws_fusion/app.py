import argparse
import logging

from importlib.metadata import version
from .commands import open_browser, iam_user_credentials, generate_okta_device_auth_credentials, init


def main():
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument('-v', '--version', action='version', help="Display the version of this tool", version=version("aws_fusion"))
    global_parser.add_argument('--debug', action='store_true', help='Turn on debug logging')

    main_parser = argparse.ArgumentParser(prog='aws-fusion', description='Unified CLI tool for streamlined AWS operations, enhancing developer productivity', parents=[global_parser])
    subparsers = main_parser.add_subparsers(dest='command', required=True, help='Available commands')

    open_browser.setup(subparsers, global_parser)
    iam_user_credentials.setup(subparsers, global_parser)
    generate_okta_device_auth_credentials.setup(subparsers, global_parser)
    init.setup(subparsers, global_parser)

    args = main_parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Call the associated function for the selected sub-command
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()
