# aws console
AWS Console Login Utility

[![Tagging](https://github.com/snigdhasjg/aws-console/actions/workflows/tagging.yml/badge.svg)](https://github.com/snigdhasjg/aws-console/actions/workflows/tagging.yml)

# Installation
## Via Pip
Install via pip install.
_note this also required git to be present_

```shell
pip install git+https://github.com/snigdhasjg/aws-console.git@main
```

## Manually
1. Simply clone this repository
```shell
git clone https://github.com/snigdhasjg/aws-console.git
```
2. Install using [setup.py](./setup.py)
```shell
python setup.py install
```

---
Post this step `aws-console` script will be added to python binary directy at `<path-to-python-installation>/bin/aws-console`

# Usage
 - Make AWS credentials available via aws profile
 - Execute the script: `aws-console --profile my-profile`
 - :tada: Your browser opens, and you are signed in into the AWS console

## Use cases
This only works with assume-role and federated-login, doesn't work with IAM user or user session.

### IAM assume role
Profiles that use IAM roles pull credentials from another profile, and then apply IAM role permissions. 

In the following examples, `iam-user` is the source profile for credentials and `iam-assume-role` borrows the same credentials then assumes a new role.

**Credentials file**
```
[profile iam-user]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Config file**
```
[profile iam-user]
region = us-east-1
output = json

[profile iam-assume-role]
source_profile = iam-user
role_arn = arn:aws:iam::777788889999:role/user-role
role_session_name = my-session
region = ap-south-1
output = json
```

### Federated login
Using IAM Identity Center, you can login to Active Directory, a built-in IAM Identity Center directory, or another IdP connected to IAM Identity Center. You can map these credentials to an AWS Identity and Access Management (IAM) role for you to run AWS CLI commands.

In the following examples, using `aws-sso` profile assumes `sso-read-only-role` on `111122223333` account.

**Config file**
```
[profile aws-sso]
sso_session = my-sso-session
sso_account_id = 111122223333
sso_role_name = sso-read-only-role
role_session_name = my-session
region = us-east-1
output = json

[sso-session my-sso-session]
sso_region = us-east-2
sso_start_url = https://my-sso-portal.awsapps.com/start
sso_registration_scopes = sso:account:access
```

> Try `aws-console --help` for detailed parameter

## Refer
The docs
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
