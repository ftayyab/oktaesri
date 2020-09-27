import requests
import json
from oktaesri.oktabroker import Broker
import time
"""
This script is a sample provided as a starter to enable developers to use the OktaBroker library in their own custom programs,
applications and scripts
User must use their own OKTA account and password to retrieve the token from the Platform.
"""
BASE_URL = 'https://.../FeatureServer/0/'

options = {'portal': 'https://.....',
               'okta_baseurl': 'https://<your tenant>.okta.com',
               'username': '',
               'password': '',
               'client_id': '',
               'redirect_uri': '',
               'expiration': 7800}

broker = Broker(options);
time.sleep(0.5)
token = broker.get_token()

r = requests.get(BASE_URL+'/query?where=1=1&resultType=&f=pjson&returnCountOnly=false&token=' + token)

print(r.status_code, r.reason)
print(json.dumps(r.text))

"""
    In case of using the ARCGIS Python API
    
    from arcgis.gis import GIS
    gis = GIS(token=<token here>)
    
    continue with the gis object as normal
"""