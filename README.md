# aws console
AWS Console Login Utility

# Usage
 - Save this script somewhere on your path (e.g. `vi /usr/local/bin/aws-console && chmod +x /usr/local/bin/aws-console`)
 - Make AWS credentials available in one of the usual places where boto3 can find them (~/.aws/credentials, env var, etc.)
 - Execute the script: `aws-console --profile my-profile`
 - :tada: Your browser opens, and you are signed in into the AWS console

## Refer
The docs: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
