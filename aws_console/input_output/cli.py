import os
import argparse


def parse_arguments():
    return __arg_parser().parse_args()


def __arg_parser():
    parser = argparse.ArgumentParser(
        description="Open the AWS console in your web browser, using your AWS CLI credentials")

    parser.add_argument('--profile', default=os.getenv("AWS_PROFILE", "joe-user"),
                        help="The AWS profile to create the pre-signed URL with")
    parser.add_argument('--region', default=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION")),
                        help="The AWS Region to send the request to")
    parser.add_argument('--stdout', action='store_true',
                        help="don't open the web browser, but echo the signin URL to stdout")

    return parser
