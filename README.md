About: This package has been provided to allow users of ArcGIS Enterprise to retrieve a token and use it with ArcGIS Rest
API and/or ArcGIS API for Python to access their content on the ArcGIS Platform.
The library allows integration through OKTA and therefore doesnt require the use of
built-in accounts. The library also handles MFA in case (if MFA is enabled).

Usage: It is essential that the user provides all the required options for successful retrieval of the token
The library maintains a log file which will save errors in case of failure and can be useful for debugging.
The user must provide the following option as:

{'portal': 'https://<domain>>.com/arcgis',
               'okta_baseurl': 'https://<domain>>.okta.com',
               'username': '<username>',
               'password': '<password>',
               'client_id': 'App Client ID',
               'redirect_uri': 'App Redirect URI',
               'expiration': required token expiration}

The library can be used with the Rest API in python scripts, jupyter notebooks (once imported) etc.
The library can also be used with the ArcGIS API for python in the GIS() class by providing token parameter
with the retrieved value (token)

Quick Sample Code;
    from oktaesri.oktabroker import Broker

    broker = Broker(options);
    time.sleep(0.5)
    token = broker.get_token()

Important:
- It is mandatory that the required Application has been pre-created on the Portal for the library to work properly.

The following items are important for the functioning of the script and must be carried out before using the library:
1. App ID (To be obtained from the Application created in the GIS Platform, in Registered Information)
2. Redirect_URI (To be obtained from the Application Registered information)
3. The item/resource (map, featurelayer etc) should be shared with the appropiate group (user access)
4. In python environment on your local machine, run pip install <path to the whl file> if a whl file is used or
   run exe file (if provided)
5. See sample.py for an example of how to call a feature service and retrieve JSON