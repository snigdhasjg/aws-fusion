import requests
import webbrowser
import time
import sys
import base64
import logging

from bs4 import BeautifulSoup

LOG = logging.getLogger(__name__)


def device_auth(org_domain, oidc_client_id):
    LOG.debug('Started device auth')
    url = "https://" + org_domain + "/oauth2/v1/device/authorize"
    payload = 'client_id=' + oidc_client_id + \
              '&scope=openid%20okta.apps.sso%20okta.apps.read'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    request = requests.post(url, headers=headers, data=payload)
    response = request.json()

    verification_url = response['verification_uri_complete']
    webbrowser.open_new_tab(verification_url)

    LOG.debug(f'Got device code {response["device_code"]}')
    return response['device_code']


def verification_and_token(org_domain, oidc_client_id, device_code):
    LOG.debug('Started verification of device code')
    url = "https://" + org_domain + "/oauth2/v1/token"
    payload = 'client_id=' + oidc_client_id + '&device_code=' + device_code + \
              '&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    while True:
        request = requests.post(url, headers=headers, data=payload)
        response = request.json()

        # Check for authorization pending
        if request.status_code == 400 and response['error'] == 'authorization_pending':
            LOG.debug('Waiting for verification')
            time.sleep(5)
            continue

        # Check for successful verification
        if request.status_code == 200:
            break

        # Unexpected state. Die.
        LOG.error(response)
        sys.exit(1)

    LOG.debug('Validated device code and got access_token & id_token')
    return response['access_token'], response['id_token']


def session_and_token(org_domain, oidc_client_id, access_token, id_token, aws_acct_fed_app_id):
    LOG.debug('Started getting of session token')
    url = "https://" + org_domain + "/oauth2/v1/token"
    payload = 'client_id=' + oidc_client_id + '&actor_token=' + access_token + \
              '&actor_token_type=urn%3Aietf%3Aparams%3Aoauth%3Atoken-type%3Aaccess_token' + \
              '&subject_token=' + id_token + \
              '&subject_token_type=urn%3Aietf%3Aparams%3Aoauth%3Atoken-type%3Aid_token' + \
              '&grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange' + \
              '&requested_token_type=urn%3Aokta%3Aoauth%3Atoken-type%3Aweb_sso_token' + \
              '&audience=urn%3Aokta%3Aapps%3A' + aws_acct_fed_app_id
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    request = requests.post(url, headers=headers, data=payload)
    response = request.json()

    LOG.debug('Got session token')
    return response['access_token']


def saml_assertion(org_domain, session_token):
    LOG.debug('Started SAML assertion')
    # Get SAML assertion
    url = 'https://' + org_domain + '/login/token/sso?token=' + session_token
    response = requests.get(url)

    # Extract response value from SAML assertion call
    parser = BeautifulSoup(response.text, "html.parser")
    saml_response = parser.find("input", {"name": "SAMLResponse"})['value']
    parser = BeautifulSoup(base64.b64decode(saml_response), features="xml")

    # Retrieve list of Roles from the SAML assertion
    roles = {}
    role_xml = parser.find("saml2:Attribute", {"Name": "https://aws.amazon.com/SAML/Attributes/Role"})
    for role in role_xml.find_all("saml2:AttributeValue"):
        idp_and_role = role.text.split(',')
        roles[idp_and_role[1]] = idp_and_role[0]

    session_duration_xml = parser.find("saml2:Attribute",
                                       {"Name": "https://aws.amazon.com/SAML/Attributes/SessionDuration"})
    session_duration = session_duration_xml.find("saml2:AttributeValue").text

    LOG.debug('Got valid SAML response')
    time.sleep(5)
    return saml_response, roles, int(session_duration)
