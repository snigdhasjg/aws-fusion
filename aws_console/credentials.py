from .cache import JSONFileCache

import boto3


class TokenGenerationException(Exception):
    "Exception for credential not having token"
    pass


def aws_credentials(profile_name):
    session = boto3.Session(profile_name=profile_name)

    # Setting up a custom cache implementation like aws cli
    cred_chain = session._session.get_component('credential_provider')
    provider = cred_chain.get_provider('assume-role')
    provider.cache = JSONFileCache()

    creds = session.get_credentials()
    if creds.token is None:
        raise TokenGenerationException()

    return creds, session.region_name
