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
