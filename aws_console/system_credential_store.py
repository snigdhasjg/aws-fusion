import keyring
import json


def store_aws_credential(account_id, username, access_key, secret_key):
    service_name = '-'.join(filter(None, ['aws', account_id, username]))
    keyring.set_password(service_name, access_key, secret_key)


def get_aws_credential(account_id, username, access_key):
    service_name = '-'.join(filter(None, ['aws', account_id, username]))
    secret_key = keyring.get_password(service_name, access_key)
    
    # https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html
    print(json.dumps({
        "Version": 1,
        "AccessKeyId": access_key,
        "SecretAccessKey": secret_key
    }))
