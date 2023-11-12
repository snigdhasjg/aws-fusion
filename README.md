# aws console
AWS Console Login Utility

[![Tag][tag-badge]][tag]
[![Tagging][actions-workflow-tagging-badge]][actions-workflow-tagging]

## Command line tool
- `aws-console`
- `aws-credential-process-from-system`

Additonally this creates [aws cli alias](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-alias.html) for all the tools
- `aws console`
- `aws credential-process-from-system`

## Installation
### Via Pip
Install via pip install.
_note this also requires git to be present_

```shell
pip install git+https://github.com/snigdhasjg/aws-console.git@main
```

### Manually
1. Simply clone this repository
```shell
git clone https://github.com/snigdhasjg/aws-console.git
```
2. Install using [setup.py](./setup.py)
```shell
python setup.py install
```

---
## Usage of `aws-console`
 - Make AWS credentials available via aws profile
 - Execute the script: `aws-console --profile my-profile`
 - :tada: Your browser opens, and you are signed in into the AWS console

### Use cases
This only works with assume-role and federated-login, doesn't work with IAM user or user session.

#### IAM assume role
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

#### Federated login
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

### Refer
The docs
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

---
## Usage of `aws-credential-process-from-system`
The tool provides two main commands: `store` and `get`.
- Store AWS credentials in system default credential store
- Retrieve AWS credentials from system default credential store. Optionally plug the CLI to aws external credential process.

### Use cases
To store IAM user credential in the system credential store for best security rather than plain text `~/.aws/credentials` file.

Manully the save the credential in the store using
```bash
aws-credential-process-from-system store \
    --access-key 'AKIAIOSFODNN7EXAMPLE' \
    --secret-key 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY' \
    --account-id '123456789012' \
    --username 'my-iam-user'
```

Configure aws config file to use credential process
**Config file**
```
[profile iam-user]
region = us-east-1
output = json
credential_process = aws-credential-process-from-system get --account-id 123456789012 --username 'my-iam-user' --access-key 'AKIAIOSFODNN7EXAMPLE'
```

> Try `aws-credential-process-from-system --help` for detailed parameter

### Refer
The docs
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html

---
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

<!-- badge links -->

[tag]: https://github.com/snigdhasjg/aws-console/tags
[tag-badge]: https://img.shields.io/github/v/tag/snigdhasjg/aws-console?style=for-the-badge&logo=github

[actions-workflow-tagging]: https://github.com/snigdhasjg/aws-console/actions/workflows/tagging.yml
[actions-workflow-tagging-badge]: https://img.shields.io/github/actions/workflow/status/snigdhasjg/aws-console/tagging.yml?branch=main&label=Tagging&style=for-the-badge&logo=githubactions
