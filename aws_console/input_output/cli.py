import os
import argparse


def parse_arguments():
    return __arg_parser().parse_args()


def __arg_parser():
    parser = argparse.ArgumentParser(
        description="Open the AWS console in your web browser, using your AWS CLI credentials")

    default_aws_profile = os.getenv("AWS_PROFILE", default="default")
    parser.add_argument('--profile', default=default_aws_profile,
                        help="The AWS profile to create the pre-signed URL with")
    parser.add_argument('--stdout', action='store_true',
                        help="don't open the web browser, but echo the signin URL to stdout")

    return parser
