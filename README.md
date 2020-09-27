# OKTA ESRI ENTERPRISE BROKER

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](http://python.org)

This library has been provided to allow users of ArcGIS Enterprise to easily retrieve a token for their scripting needs. This token can be used with ArcGIS Rest API and/or ArcGIS API for Python. ArcGIS Enterprise does not provide out of the box solution to retrieve a token (when OKTA integration is setup). The only option is to use built-in accounts. However this may not be suitable in some cases as it adds a account and group management overhead. 

This library works as a broker and will allow users to access their content on the ArcGIS Platform using their OKTA based crendetails without the need of creating or requesting a built-in account. This allows the user to work with their content in their own groups without the need to create built-in accounts.

The library also handles MFA in case (if MFA is enabled)

# New Features!

  - Inclusion of MFA two factor authentication (Must be accepted within 30 seconds)
  - Error Logging


You can also:
  - Use the library with jupyter notebook and Python API GIS(token=) objects 

# Usage
It is essential, the user provides all the required options for successful retrieval of the token
The user must provide the following option as:

* Portal url
* okta base url
* username
* password
* client_id
* redirect_id
* expiration (optional)

## Code
```sh
 from oktaesri.oktabroker import Broker

    broker = Broker(options);
    time.sleep(0.5)
    token = broker.get_token()
```
## Important
- It is mandatory that the required Application has been pre-created on the Portal for the library to work properly.

The following items are important for the functioning of the script and must be carried out before using the library:
1. App ID (To be obtained from the Application created in the GIS Platform, in Registered Information)
2. Redirect_URI (To be obtained from the Application Registered information)
3. The item/resource (map, featurelayer etc) should be shared with the appropiate group (user access)
4. Python Installed on your machine (version 3.7 and above)
5. See sample.py (for detailed code example)

### Installation

If you want to install the library for your own use please see below: [Usage terms apply]
Note: pip must be installed and available
```sh
run batch file provided in the zip file.
```

License
----

Copyright (c) 2020 faizantayyab.com - All Rights Reserved

Unauthorized copying of this product/library, via any medium is strictly prohibited
Available for free non-commercial usage
For commercial use please contact the author
Written by Faizan Tayyab <faizantayyab.com>, September 2020


The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
----

### Contact
Author can be contacted via http://www.faizantayyab.com & linkedin
