import json
from urllib import parse
from urllib import request


ISSUER = "aws-console-python-script"
SESSION_DURATION_IN_SECONDS = 43200


def signin_url(creds, region_name):
    login_request_url = __aws_login_url(
        creds.access_key, creds.secret_key, creds.token, region_name)
    return 'https://us-east-1.signin.aws.amazon.com/oauth?Action=logout' \
        f'&redirect_uri={parse.quote_plus(login_request_url)}'


def __aws_signin_token(access_key, secret_key, session_token) -> str:
    url_credentials = dict(sessionId=access_key,
                           sessionKey=secret_key, sessionToken=session_token)
    credentials_encoded = parse.quote_plus(json.dumps(url_credentials))
    request_url = 'https://signin.aws.amazon.com/federation?Action=getSigninToken' \
                  f'&Session={credentials_encoded}'  # f'&SessionDuration={SESSION_DURATION_IN_SECONDS}'

    with request.urlopen(request_url) as response:
        if not response.status == 200:
            raise Exception("Failed to get federation token")
        return json.loads(response.read())["SigninToken"]


def __aws_login_url(access_key, secret_key, session_token, region_name) -> str:
    destination_url_encoded = parse.quote_plus(
        "https://{}.console.aws.amazon.com/".format(region_name))
    signin_token_encoded = parse.quote_plus(
        __aws_signin_token(access_key, secret_key, session_token))
    return 'https://us-east-1.signin.aws.amazon.com/federation?Action=login' \
           f'&Issuer={ISSUER}' \
           f'&Destination={destination_url_encoded}' \
           f'&SigninToken={signin_token_encoded}'
