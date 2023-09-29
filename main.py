#!/opt/homebrew/anaconda3/bin/python

"""
Refer:
 - The docs: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
Usage:
 - Save this script somewhere on your path (e.g. `vi /usr/local/bin/aws-console && chmod +x /usr/local/bin/aws-console`)
 - Make AWS credentials available in one of the usual places where boto3 can find them (~/.aws/credentials, env var, etc.)
 - Execute the script: `aws-console --profile my-profile`
 - :tada: Your browser opens, and you are signed in into the AWS console
"""

import webbrowser

from aws.helper import signin_url
from argument.inputs import get_arguments

def open_console(profile_name, echo_to_stdout):
    with_logout_request_url = signin_url(profile_name)

    if echo_to_stdout:
        print(with_logout_request_url)
    else:
        webbrowser.open(with_logout_request_url)


if __name__ == '__main__':
    args = get_arguments()
    open_console(args.profile, args.stdout)
