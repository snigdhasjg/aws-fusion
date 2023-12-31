import argparse
import logging
from importlib.metadata import version

from .commands import (
    init,
    open_browser,
    config_switch,
    iam_user_credentials,
    okta
)


def main():
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument('-v', '--version', action='version', help="Display the version of this tool", version=version("aws_fusion"))
    global_parser.add_argument('--debug', action='store_true', help='Turn on debug logging')

    main_parser = argparse.ArgumentParser(prog='aws-fusion', description='Unified CLI tool for streamlined AWS operations, enhancing developer productivity', parents=[global_parser])
    subparsers = main_parser.add_subparsers(dest='command', required=True, help='Available commands')

    commands = [
        init,
        open_browser,
        iam_user_credentials,
        okta,
        config_switch
    ]
    [command.setup(subparsers, global_parser) for command in commands]

    args = main_parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Call the associated function for the selected sub-command
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == '__main__':
    main()
