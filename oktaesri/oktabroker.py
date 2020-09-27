"""
    Python package
    Purpose: Broker to act as a bridge between client and ESRI Enterprise Implementation
    Developed By: http://faizantayyab.com
    Created 26/09/2020
"""
import sys

from oktaesri.authorization import Authorization
# Imports
from oktaesri.logger import Logger
from oktaesri.remote import *
from oktaesri.settings import *


class Broker:
    """
        Broker class contains logic to retrieve token from Enterprise
    """


    def __init__(self, options):

        # Initialize variable

        self.portal = None
        self.username = None
        self.password = None
        self.client_id = None
        self.redirect_uri = None
        self.expiration = None
        self.okta_baseurl = None
        self.authorization = Authorization()


        self.INVALID_URL_ERROR = {'code': -1, 'message': 'Invalid URL'}
        self.INVALID_OR_MISSING_PARAMETERS = {'code': 1, 'message': 'Invalid or Missing Parameter(s)'}
        self.UNHEALTHY_PORTAL = {'code': -1, 'message': 'Unhealthy Portal or Invalid URL'}

        # Check Input (sanitize)
        sanitize_result = self.sanitize_input(options['portal'], options['okta_baseurl'], options['username'],
                                              options['password'], options['client_id'], options['redirect_uri'],
                                              options['expiration'])
        if not sanitize_result:
            self.configure()
        else:
            Logger.write_2_log(sanitize_result)
            sys.exit(sanitize_result['code'])

    def configure(self):
        """
        Store user provided configurations
        :param okta_base_endpoint
        :param portal:
        :return:
        """

        Globals.configurations['ClientAuthorization']['authorize_url'] = self.portal + '/sharing/rest/oauth2/saml/authorize'
        Globals.configurations['ClientAuthorization']['expiration'] = self.expiration
        Globals.configurations['ClientAuthorization']['client_id'] = self.client_id
        Globals.configurations['ClientAuthorization']['redirect_uri'] = self.redirect_uri
        Globals.configurations['ClientAuthorization']['expiration'] = self.expiration

        #print(Globals.configurations['ClientAuthorization'])

        Globals.configurations['CookieRedirect']['redirect_endpoint'] = self.okta_baseurl + '/login/sessionCookieRedirect'

        #print(Globals.configurations['CookieRedirect'])

        Globals.configurations['OKTAAuthentication']['endpoint'] = self.okta_baseurl + '/api/v1/authn'

        #print(Globals.configurations['OKTAAuthentication'])

        Globals.configurations['SAMLSignin']['SAMLResponse'] = ''
        Globals.configurations['SAMLSignin']['RelayState'] = ''
        Globals.configurations['SAMLSignin']['endpoint'] = self.portal + '/sharing/rest/oauth2/saml/signin'

        #print(Globals.configurations['SAMLSignin'])

        Globals.configurations['OauthToken']['endpoint'] = self.portal + '/sharing/rest/oauth2/token'

        #print(Globals.configurations['OauthToken'])



    def check_enterprise(self, portal):
        """
        Verifies Portal is accessible
        :param portal:
        :param url
        :return 1 or 0:
        """
        return Remote.make_get_call(portal + '/portaladmin/healthCheck?f=json')

    def sanitize_input(self, portal=None, okta_baseurl=None, username=None, password=None, client_id=None,
                       redirect_uri=None, expiration=1000):
        """

        :param expiration:
        :param okta_base_endpoint:
        :param portal:
        :param username:
        :param password:
        :param client_id:
        :param redirect_uri:
        :return Error or confirmation:

        """
        client_parameters_errors = None;
        if portal is not None and len(portal) > 0 and portal.startswith('http'):
            if portal.endswith('/'):
                portal = portal[:-1]
            if self.check_enterprise(portal):
                self.portal = portal.strip()
            else:
                client_parameters_errors = self.UNHEALTHY_PORTAL
        else:
            self.INVALID_OR_MISSING_PARAMETERS

        if okta_baseurl is not None and len(okta_baseurl) > 0 and okta_baseurl.startswith('http'):
            if okta_baseurl.endswith('/'):
                okta_baseurl = okta_baseurl[:-1]
            self.okta_baseurl = okta_baseurl.strip()
        else:
            self.INVALID_OR_MISSING_PARAMETERS

        if username is not None and len(username) > 0:
            self.username = username.strip()
        else:
            client_parameters_errors = self.INVALID_OR_MISSING_PARAMETERS

        if password is not None and len(password) > 0:
            self.password = password.strip()
        else:
            client_parameters_errors = self.INVALID_OR_MISSING_PARAMETERS

        if client_id is not None and len(client_id) > 0:
            self.client_id = client_id.strip()
        else:
            client_parameters_errors = self.INVALID_OR_MISSING_PARAMETERS

        if redirect_uri is not None and len(redirect_uri) > 0:
            self.redirect_uri = redirect_uri.strip()
        else:
            client_parameters_errors = self.INVALID_OR_MISSING_PARAMETERS

        self.expiration = expiration

        return None if client_parameters_errors is None else client_parameters_errors

    def get_token(self):
        """
        Proceed with getting token if no errors found
        :return: Generated Token
        """
        try:
            if self.username is None or self.password is None:
                raise Exception('Credentials are missing')
            else:
                token = self.authorization.authorize_client(self.username, self.password)
                return token
        except Exception as e:
            return None
