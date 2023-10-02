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

 > Try `aws-console --help` for detailed parameter

## Refer
The docs: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html
