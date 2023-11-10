from botocore.utils import JSONFileCache
import boto3

import datetime
import os
import json


class TokenGenerationException(Exception):
    "Exception for credential not having token"
    pass


def aws_session_credential(profile_name, region_name):
    session = boto3.Session(profile_name=profile_name, region_name=region_name)

    __update_credential_provider_cache(session)

    creds = session.get_credentials()
    if creds.token is None:
        raise TokenGenerationException()

    return creds, session.region_name


def __update_credential_provider_cache(session):
    "Setting up a custom cache implementation like aws cli"

    cred_chain = session._session.get_component('credential_provider')
    jsonFileCache = JSONFileCache()

    def _update(provider_name):
        cred_chain.get_provider(provider_name).cache = jsonFileCache

    provider_for_cache = [
        'assume-role',
        'assume-role-with-web-identity',
        'sso'
    ]

    [_update(each_provider) for each_provider in provider_for_cache]