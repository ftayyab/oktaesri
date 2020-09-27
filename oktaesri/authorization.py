"""
Purpose: Class for Authorization logic
"""

import sys
import time

from bs4 import BeautifulSoup

from oktaesri.logger import Logger
from oktaesri.remote import *
from oktaesri.settings import *


class Authorization:
    def __init__(self):
        self.username = None
        self.password = None


    # oAuth Token

    def oauth_token_failure(self, err):
        if err and err.message:
            Logger.write_2_log(err.message)
        sys.exit(-1)

        # ESRI Token
    def oauth_token_success(self, res):
        """
        :param res: Pass in the response
        :return Portal GIS Token:
        """
        token = self.parse_oauth_token(res)
        if len(token) > 0 and token is not None:
            return token
        else:
            Logger.write_2_log('Unable to generate Token')
            sys.exit(-1)


    def parse_oauth_token(self, content):
        """
        :param content: Pass in the content
        :return: return the Access Token
        """
        try:
            if 'error' not in content:
                parsed_html = BeautifulSoup(content, features='html.parser')
                access_token = json.loads(content)['access_token']
                if access_token is not None:
                    return access_token
            else:
                Logger.write_2_log('Unable to generate the Access Token')
                sys.exit(-1)
        except:
            Logger.write_2_log('Unable to retrieve code [parse_oauth_token]')
            sys.exit(-1)

    def get_token(self):
        """
        :param resolve:
        :param reject:
        :return: Method to retrieve the GIS Token
        """

        settings = Globals.configurations['OauthToken']

        url = None
        params = None
        url = settings['endpoint']
        settings.pop('endpoint', None)
        params = settings

        params['client_id'] = Globals.configurations['ClientAuthorization']['client_id']
        params['redirect_uri'] = Globals.configurations['ClientAuthorization']['redirect_uri']

        response = Remote.make_post_call(url, params)

        if response['status'] == 200:
            return self.oauth_token_success(response['payload'])
        else:
            self.oauth_token_failure(response['payload'])

    def oauth_token(self, params):
        if len(params) > 0:
            Globals.configurations['OauthToken']['code'] = params['code']
            #print(Globals.configurations['OauthToken'])
            return self.get_token()
        else:
            Logger.write_2_log('Unable to retrieve code [Ouath_token function]')
            sys.exit('Errors Logged')

    # SAML OAUTH
    def parse_oauth_signin(self, content):
        try:
            parsed_html = BeautifulSoup(content, features='html.parser')
            code = parsed_html.find_all('input')[0]['value']
            return {'code': code}
        except:
            return None

    def oauth_singin_success(self, res):
        params = self.parse_oauth_signin(res)
        if params is not None:
            return self.oauth_token(params)
        else:
            self.oauth_signin_failure(None)

    def oauth_signin_failure(self, err):
        Logger.write_2_log('Unable to retrieve Code [Parse Oauth signin function]')
        sys.exit(-1)

    def oauth_signin(self):
        settings = Globals.configurations['SAMLSignin']
        url = None
        params = None
        url = settings['endpoint']
        settings.pop('endpoint', None)
        params = settings
        response = Remote.make_post_call(url, params)
        payload = response['payload']
        try:
            parsed_html = BeautifulSoup(payload, features='html.parser')

            if response['status'] == 200 and 'code' in str(parsed_html.title):
                return self.oauth_singin_success(response['payload'])
            else:
                self.oauth_signin_failure(response['payload'])
        except Exception as e:
            Logger.write_2_log('Unable to make OAuth signin [Func: oauth_signin]')
            sys.exit(-1)

    def oauth_saml_signin(self, params):
        Globals.configurations['SAMLSignin']['SAMLResponse'] = params['SAMLResponse']
        Globals.configurations['SAMLSignin']['RelayState'] = params['RelayState']
        #print(Globals.configurations['SAMLSignin'])
        return self.oauth_signin()

    # Exchange token
    def parse_exchange_cookie(self, content):
        """
        :param content:
        :return: Return SAML Response + Relay State or error
        """
        try:
            parsed_html = BeautifulSoup(content, features='html.parser')
            SAMLResponse = parsed_html.find_all('input')[0]['value']
            RelayState = parsed_html.find_all('input')[1]['value']

            if 'Signing' in str(parsed_html.title):
                return {'SAMLResponse': parsed_html.find_all('input')[0]['value'],
                        'RelayState': parsed_html.find_all('input')[1]['value']}
            else:
                return {'Error': 'Unable to complete request'}
        except:
            return None

    def session_cookie_exchange_success(self, res):
        params = self.parse_exchange_cookie(res)
        if params is not None:
            if 'Error' in params.keys():
                Logger.write_2_log('Unable to complete request')
                sys.exit('Errors Logged')
            else:
                return self.oauth_saml_signin(params)
        else:
            Logger.write_2_log('Unable to make Authorization Call [Func: session cookie xchange]')
            sys.exit(-1)

    def session_cookie_exchange_failure(self, err):
        Logger.write_2_log(err)
        sys.exit(-1)

    def session_cookie_exchange(self, params):

        Globals.configurations['CookieRedirect']['token'] = params['token']

        #print(Globals.configurations['CookieRedirect'])
        return self.exchange_cookie()

    def exchange_cookie(self):
        """
        XChange OKTA credential with Portal
        """
        settings = Globals.configurations['CookieRedirect']

        url = None
        params = None

        if settings is not None:
            url = settings['redirect_endpoint']
            settings.pop('redirect_endpoint', None)
            params = settings

            response = Remote.make_post_call(url, params)

            if response['status'] == 200:
                return self.session_cookie_exchange_success(response['payload'])
            else:
                self.session_cookie_exchange_failure(
                    response['payload'] + ' Unable to exchange cookies [Func: Exchange Cookie] ')
        else:
            Logger.write_2_log('Unable to exchange cookies [Func: Exchange Cookie]')
            sys.exit(-1)

    def handle_mfa(self, state, factor, url):
        params = {'stateToken': state}
        url = "{0}/factors/{1}/verify".format(url, factor)
        result = Remote.make_post_json_call(url, params)
        count = 0
        while json.loads(result['payload'])['status'] == 'MFA_CHALLENGE':
            time.sleep(5)
            if count >= 5:
                count = 0
                Logger.write_2_log('Unable to get MFA from device [Func: MFA Error]');
                sys.exit('No MFA code provided for 30 seconds, existing')
            count = count + 1
            result = Remote.make_post_json_call(url, params)
        if json.loads(result['payload'])['status'] == 'SUCCESS':
            return json.loads(result['payload'])['sessionToken']
        else:
            Logger.write_2_log('Unable to get MFA from device [Func: MFA Error]');
            sys.exit('No MFA code provided for 30 seconds, existing')

    # User Authorization in OKTA

    def authenticate_success(self, res, url):

        try:
            res = json.loads(res)
            status = res['status']
            factor = res['_embedded']['factors'][0]['id']
            state = res['stateToken']

            if status == 'MFA_REQUIRED':
                params = {'token': self.handle_mfa(state, factor, url)}
                return self.session_cookie_exchange(params)
            else:
                if res is not None:
                    params = {'token': json.loads(res)['sessionToken']}
                    return self.session_cookie_exchange(params)
                else:
                    Logger.write_2_log('Unable to Authenticate against OKTA [Func: Authenticate User]');
                    sys.exist('Errors Logged')

        except Exception as e:
            Logger.write_2_log('Unable to Authenticate against OKTA [Func: Authenticate User]');
            sys.exist(-1)

    def authenticate_failure(self, err):
        Logger.write_2_log(err)
        sys.exit(-1)

    def okta_authentication(self, params):
        """
        OKTA Authentication (Account per user and should exist in group)
        """
        settings = Globals.configurations['OKTAAuthentication']
        url = settings['endpoint']
        if self.username is not None and self.password is not None:
            params = {'username': self.username, 'password': self.password}
            response = Remote.make_post_json_call(url, params)
            if response['status'] == 200:
                return self.authenticate_success(response['payload'], url)
            else:
                self.authenticate_failure(response['payload'] + ' or Invalid credentials')
        else:
            self.authenticate_failure('Unable to Retrieve User/Session Token [Func: Authenticate User]')

    # App authorization
    def parse_authorization_app_response(self, content):
        """
        :param content:
        :return parsed & extracted content:
        """
        try:
            parsed_html = BeautifulSoup(content, features='html.parser')
            return {'redirectUrl': parsed_html.find_all('input')[1]['value']}
        except Exception as e:
            return None

    def authorize_app_success(self, res):
        """
        :param res:
        :return okta authentication response:
        """
        params = self.parse_authorization_app_response(res)

        if params is None:
            Logger.write_2_log('Unable to make Authorization Call [Func: authorize Client]')
            sys.exit(-1)
        else:
            Globals.configurations['CookieRedirect']['redirectUrl'] = params['redirectUrl']
            #print(Globals.configurations['CookieRedirect'])
            return self.okta_authentication(params)


    def authorize_app_failure(self, err):
        if '<title>' in str(err):
            startIdx = err.find('<title>')
            endIdx = err.find('</title>')
            Logger.write_2_log(str(err[startIdx + 7:endIdx]) + " [Func: authorize App]")
        else:
            Logger.write_2_log('Unable to make Authorization Call [Func: authorize App]')
        sys.exit(-1)

    def okta_app_authorization(self, params):
        """
        Client Authorization with ArcGIS based on AppID from application created on Portal
        """
        url = None
        params = None
        settings = Globals.configurations['OKTAAppAuthorization']

        if settings is not None:
            url = settings['endpoint']
            settings.pop('endpoint', None)
            params = settings

            response = Remote.make_post_call(url, params)

            if response['status'] == 200:
                return self.authorize_app_success(response['payload'])
            else:
                self.authorize_app_failure(response['payload'])
        else:
            self.authorize_app_failure('Unable to make Authorization Call [Func: authorize App]')

    # Authorize Client
    def parse_authorization_client_response(self, content):
        """
        :param content:
        :return Extract SAML properties:
        """
        try:
            parsed_html = BeautifulSoup(content, features='html.parser')
            okta_app_endpoint = parsed_html.form['action']
            SAMLRequest = parsed_html.find_all('input')[0]['value']
            RelayState = parsed_html.find_all('input')[1]['value']
            return {'endpoint': okta_app_endpoint, 'SAMLRequest': SAMLRequest, 'RelayState': RelayState}
        except Exception as e:
            return None

    def authorize_client_success(self, res):
        """
        :param res: response
        :return okta app authorization:
        """
        params = self.parse_authorization_client_response(res)

        if params is None:
            Logger.write_2_log('Unable to make Authorization Call [Func: authorize Client]')
            sys.exit(-1)
        else:

            if 'endpoint' in params:
                Globals.configurations['OKTAAppAuthorization']['endpoint'] = params['endpoint']
                Globals.configurations['OKTAAppAuthorization']['SAMLRequest'] = params['SAMLRequest']
                Globals.configurations['OKTAAppAuthorization']['RelayState'] = params['RelayState']
                #print(Globals.configurations['OKTAAppAuthorization'])
                return self.okta_app_authorization(params)
            else:
                Logger.write_2_log('Unable to make Authorization Call [Func: authorize Client]')
                sys.exit(-1)

    def authorize_client_failure(self, err):
        """
        :param err:
        :return: None
        """
        try:
            if '<title>' in str(err):
                startIdx = err.find('<title>')
                endIdx = err.find('</title>')
                Logger.write_2_log(str(err[startIdx + 7:endIdx]) + " [Func: authorize Client]")
            else:
                raise Exception()
        except Exception as e:
            Logger.write_2_log(str(err) + '[Func: authorize Client]')
        sys.exit(-1)

    def authorize_client(self, username, password):
        """
        Client Authorization with ArcGIS based on AppID from application created on Portal
        """
        self.username = username
        self.password = password

        url = None
        params = None
        settings = Globals.configurations['ClientAuthorization']

        if settings is not None:
            url = settings['authorize_url']
            settings.pop('authorize_url', None)
            params = settings

            response = Remote.make_post_call(url, params)

            if response['status'] == 200:
                return self.authorize_client_success(response['payload'])
            else:
                self.authorize_client_failure(response['payload'])
        else:
            self.authorize_client_failure('Unable to make Authorization Call [Func: authorize Client]')
