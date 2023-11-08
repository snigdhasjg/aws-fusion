import os
import argparse


def open_console_arguments():
    parser = argparse.ArgumentParser(
        description="Open the AWS console in your web browser, using your AWS CLI credentials")

    parser.add_argument('-v', '--version', action='store_true',
                        help="Display the version of this tool")
    parser.add_argument('-P', '--profile', default=os.getenv("AWS_PROFILE"),
                        help="The AWS profile to create the pre-signed URL with")
    parser.add_argument('-R', '--region', default=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")),
                        help="The AWS Region to send the request to")

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--clip', action='store_true',
                        help="don't open the web browser, but copy the signin URL to clipboard")
    group1.add_argument('--stdout', action='store_true',
                        help="don't open the web browser, but echo the signin URL to stdout")

    return parser.parse_args()


def credential_process_arguments():
    parser = argparse.ArgumentParser(
        description='AWS Credential Management CLI')

    parser.add_argument('-v', '--version', action='store_true',
                        help="Display the version of this tool")

    subparsers = parser.add_subparsers(
        dest='command', help='Available commands')

    # Subparser for 'store' command
    store_parser = subparsers.add_parser('store', help='Store AWS credentials')
    store_parser.add_argument(
        '--account-id', required=False, help='AWS Account ID for the name')
    store_parser.add_argument(
        '--username', required=False, help='Username of a AWS user associated with the access key for the name')
    store_parser.add_argument(
        '--access-key', required=True, help='AWS access key')
    store_parser.add_argument(
        '--secret-key', required=True, help='AWS secret key')

    # Subparser for 'get' command
    get_parser = subparsers.add_parser('get', help='Get AWS credentials')
    get_parser.add_argument(
        '--account-id', required=False, help='AWS Account ID for the name')
    get_parser.add_argument(
        '--username', required=False, help='Username of a AWS user associated with the access key for the name')
    get_parser.add_argument(
        '--access-key', required=True, help='AWS access key')
    get_parser.add_argument(
        '--credential-process', action='store_true', help='Use credential process')

    return parser.parse_args()
