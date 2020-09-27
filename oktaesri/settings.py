"""
Class to hold global settings
"""


class Globals:
    configurations = {
        'ClientAuthorization': {
            'authorize_url': '',
            'client_id': '',
            'response_type': 'code',
            'expiration': 7800,
            'redirect_uri': ''
        },
        'CookieRedirect': {
            'checkAccountSetupComplete': True,
            'repost': True,
            'token': '',
            'redirect_endpoint': '',
            'redirectUrl': ''
        },
        'OauthToken':{
            'endpoint': '',
            'code': '',
            'grant_type': 'authorization_code'
        },
        'SAMLSignin': {
            'SAMLResponse': '',
            'RelayState': '',
            'endpoint': ''
        },
        'OKTAAppAuthorization':{
            'endpoint': '',
            'SAMLRequest': '',
            'RelayState': ''
        },
        'OKTAAuthentication':{
            'endpoint':''
        }
    }

    def __init__(self):
        pass
