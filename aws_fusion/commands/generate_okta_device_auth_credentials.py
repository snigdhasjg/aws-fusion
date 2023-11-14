import os
import logging

from ..aws.assume_role import AssumeRoleWithSamlCache
from ..okta.api import device_auth, verifiction_and_token, session_and_token, saml_assertion

LOG = logging.getLogger(__name__)

def setup(subparsers, parent_parser):
    summary = 'Generate AWS session credentials using SAML assertion from Okta device authentication'
    parser = subparsers.add_parser('generate-okta-device-auth-credentials', description=summary, help=summary, parents=[parent_parser])

    parser.add_argument('--org-domain', required=True, help="Full domain hostname of the Okta org e.g. example.okta.com")
    parser.add_argument('--oidc-client-id', required=True, help="The ID is the identifier of the client is Okta app acting as the IdP for AWS")
    parser.add_argument('--aws-acct-fed-app-id', required=True, help="ID for the AWS Account Federation integration app")
    parser.add_argument('--aws-iam-role', required=True, help="The AWS IAM Role ARN to assume")
    parser.add_argument('--credential-process', action='store_true', help='Output the credential in AWS credential process syntax')

    parser.set_defaults(func=run)
    
def run(args):
    assume_role_with_cache = AssumeRoleWithSamlCache(args.aws_iam_role)

    if not assume_role_with_cache.does_valid_token_cache_exists():
        LOG.debug('Credential cache not found, invloking SAML')
        device_code = device_auth(args.org_domain, args.oidc_client_id)
        access_token, id_token = verifiction_and_token(args.org_domain, args.oidc_client_id, device_code)
        session_token = session_and_token(args.org_domain, args.oidc_client_id, access_token, id_token, args.aws_acct_fed_app_id)
        saml_response, roles, sessoion_duration = saml_assertion(args.org_domain, session_token)
        assume_role_with_cache.assume_role_with_saml(saml_response, roles, sessoion_duration)

    if args.credential_process:
        print(assume_role_with_cache.credential_process())
    