# aws fusion
Unified CLI tool for streamlined AWS operations, enhancing developer productivity

[![Tag][tag-badge]][tag]
[![Publish][actions-workflow-publish-badge]][actions-workflow-publish]

## Installation
Install via pip install

```shell
pip install aws-fusion
```

## Command line tool
To invoke the cli, there are 2 option
1. Directly use `aws-fusion` command
2. Use it via [aws cli alias](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-alias.html) with `aws fusion`

## Commands
- [init](#usage-of-init)
- [open-browser](#usage-of-open-browser)
- store-iam-user-credentials
  - [store](#usage-of-iam-user-credentials-store)
  - [get](#usage-of-iam-user-credentials-get)
- [get-iam-user-credentials](#usage-of-get-iam-user-credentials)
- [generate-okta-device-auth-credentials](#usage-of-generate-okta-device-auth-credentials)
- [config-switch](#usage-of-config-switch)
  - profile
  - region

---
## Usage of `init`
> Try `aws-fusion init --help` for detailed parameter

Initilize fusion app with creation of aws fusion alias

---
## Usage of `open-browser`
> Try `aws-fusion open-browser --help` for detailed parameter

- Make AWS credentials available via aws profile 
- Execute the script: `aws-fusion open-browser --profile my-profile`
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
Using IAM Identity Center, you can log in to Active Directory, a built-in IAM Identity Center directory, or another IdP connected to IAM Identity Center. You can map these credentials to an AWS Identity and Access Management (IAM) role for you to run AWS CLI commands.

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

### Refer
The docs
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

---
## Usage of `iam-user-credentials store`
> Try `aws-fusion iam-user-credentials store --help` for detailed parameter

Store AWS credentials in system default credential store

### Use cases
To store IAM user credential in the system credential store for best security rather than plain text `~/.aws/credentials` file.

Manually the save the credential in the store using
```bash
aws-fusion iam-user-credentials store \
    --access-key 'AKIAIOSFODNN7EXAMPLE' \
    --secret-key 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY' \
    --account-id '123456789012' \
    --username 'my-iam-user'
```

---
## Usage of `iam-user-credentials get`
> Try `aws-fusion iam-user-credentials get --help` for detailed parameter

Retrieve AWS credentials from system default credential store. Optionally plug the CLI to aws external credential process.

### Use cases
Configure aws config file to use credential process

**Config file**
```
[profile iam-user]
region = us-east-1
output = json
credential_process = aws-fusion iam-user-credentials get --account-id 123456789012 --username 'my-iam-user' --access-key 'AKIAIOSFODNN7EXAMPLE' --credential-process
```

### Refer
The docs
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html

---
## Usage of `generate-okta-device-auth-credentials`
> Try `aws-fusion generate-okta-device-auth-credentials --help` for detailed parameter

Simplifies the process of obtaining AWS session credentials using SAML assertion from Okta device authentication

### Use cases
Configure aws config file to use credential process

**Config file**
```
[profile iam-user]
region = us-east-1
output = json
credential_process = aws-fusion generate-okta-device-auth-credentials --org-domain my.okta.com --oidc-client-id 0pbs4fq1q2vbGoFkC1m7 --aws-acct-fed-app-id 0oa8z9xa8BS9b2AFb1t7 --aws-iam-role arn:aws:iam::123456789012:role/PowerUsers --credential-process
```

---
## Usage of `config-switch`
A special of utility script to help easily switch `profile` and `region`

This works with 2 bash script, namely `_awsp` and `_awsr`
> _Using the command without the bash script will have no effect_

Post installing the app, create 2 aliases in `.bashrc` or `.zshrc` file.
```shell
## aws fusion setup
alias awsp="source _awsp"
alias awsr="source _awsr"
```

---
## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

<!-- badge links -->

[tag]: https://github.com/snigdhasjg/aws-fusion/tags
[tag-badge]: https://img.shields.io/github/v/tag/snigdhasjg/aws-fusion?style=for-the-badge&logo=github

[actions-workflow-publish]: https://github.com/snigdhasjg/aws-fusion/actions/workflows/publish.yml
[actions-workflow-publish-badge]: https://img.shields.io/github/actions/workflow/status/snigdhasjg/aws-fusion/publish.yml?branch=main&label=Publish&style=for-the-badge&logo=githubactions
