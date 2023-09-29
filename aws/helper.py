from urllib import parse, request
from cache.file_cache import JSONFileCache

import botocore.credentials
import boto3
import json

ISSUER = "aws-console-python-script"
SESSION_DURATION_IN_SECONDS = 43200


def signin_url(profile_name):
    creds, region_name = __aws_credentials(profile_name)

    login_request_url = __aws_login_url(
        creds.access_key, creds.secret_key, creds.token, region_name)
    return 'https://us-east-1.signin.aws.amazon.com/oauth?Action=logout' \
        f'&redirect_uri={parse.quote_plus(login_request_url)}'


def __aws_credentials(profile_name):
    session = boto3.Session(profile_name=profile_name)

    # Setting up a custom cache implementation like aws cli
    cred_chain = session._session.get_component('credential_provider')
    provider = cred_chain.get_provider('assume-role')
    provider.cache = JSONFileCache()

    creds = session.get_credentials()
    if creds.token is None:
        credentials = session.client('sts').get_session_token()['Credentials']
        creds = botocore.credentials.Credentials(
            credentials['AccessKeyId'], credentials['SecretAccessKey'], credentials['SessionToken'])

    return creds, session.region_name


def __aws_signin_token(access_key, secret_key, token) -> str:
    url_credentials = dict(sessionId=access_key,
                           sessionKey=secret_key, sessionToken=token)
    credentials_encoded = parse.quote_plus(json.dumps(url_credentials))
    request_url = 'https://signin.aws.amazon.com/federation?Action=getSigninToken' \
                  f'&SessionDuration={SESSION_DURATION_IN_SECONDS}' \
                  f'&Session={credentials_encoded}'

    with request.urlopen(request_url) as response:
        if not response.status == 200:
            raise Exception("Failed to get federation token")
        return json.loads(response.read())["SigninToken"]


def __aws_login_url(access_key, secret_key, token, region_name) -> str:
    destination_url_encoded = parse.quote_plus(
        "https://{}.console.aws.amazon.com/".format(region_name))
    signin_token_encoded = parse.quote_plus(
        __aws_signin_token(access_key, secret_key, token))
    return 'https://us-east-1.signin.aws.amazon.com/federation?Action=login' \
           f'&Issuer={ISSUER}' \
           f'&Destination={destination_url_encoded}' \
           f'&SigninToken={signin_token_encoded}'
