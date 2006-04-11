"""Python wrapper for AWS E-Commerce Serive APIs.

Based upon pyamazon ( http://www.josephson.org/projects/pyamazon/ ) with 
efforts to meet the latest AWS specification.

The Amazon's web APIs specication is described here:
  http://www.amazon.com/webservices

You need a Amazon-provided license key to use these services.
Follow the link above to get one.  These functions will look in
several places (in this order) for the license key:
- the "license_key" argument of each function
- the module-level LICENSE_KEY variable (call setLicense once to set it)
- an environment variable called AMAZON_LICENSE_KEY


TODO: 
  - Add more decriptions about this module. 
"""

import urllib, os

__author__ = "Kun Xi < kunxi@kunxi.org >"
__version__ = "0.0.1"
__license__ = "GPL"


LICENSE_KEY = None;
HTTP_PROXY = None
LOCALE = "us"

_supportedLocales = {
        "us" : (None, "webservices.amazon.com"),   
        "uk" : ("uk", "webservices.amazon.co.uk"),
        "de" : ("de", "webservices.amazon.de"),
        "jp" : ("jp", "webservices.amazon.co.jp"),
        "fr" : ("fr", "webservices.amazon.fr"),
        "ca" : ("ca", "webservices.amazon.ca" )
    }

_licenseKeys = (
    (lambda key: key ),
    (lambda key: LICENSE_KEY ), 
    (lambda key: os.environ.get('AWS_LICENSE_KEY', None))
    )

class AWSException( Exception ) : pass
class NoLiceseException( AWSException ) : pass

def _checkLocaleSupported(locale):
    if not _supportedLocales.has_key(locale):
        raise AmazonError, ("Unsupported locale. Locale must be one of: %s" %
            string.join(_supportedLocales, ", "))

def setLocale(locale):
    """set locale"""
    global LOCALE
    _checkLocaleSupported(locale)
    LOCALE = locale

def getLocale(locale=None):
    """get locale"""
    return locale or LOCALE

def setLicenseKey(license_key):
    """set license key"""
    global LICENSE_KEY
    LICENSE_KEY = license_key

def getLicenseKey(license_key = None):
    """get license key

    license key can come from any number of locations;
    see module docs for search order"""
    for get in _licenseKeys:
        rc = get(license_key)
        if rc: 
            return rc
    raise NoLicenseKey, 'get a license key at http://www.amazon.com/webservices'

def buildURL(operation, search_index, keywords, license_key, locale, associate):
    _checkLocaleSupported(locale)
    url = "http://" + _supportedLocales[locale][1] + "/onca/xml?Service=AWSECommerceService"
    url += "&AWSAccessKeyId=%s" % license_key.strip()
    url += "&Operation=%s" % operation
    url += "&SearchIndex=%s" % search_index 
    url += "&Keywords=%s" % urllib.quote(keywords)
    return url


## main functions

if __name__ == "__main__":
    print buildURL("ItemSearch", "Books", "Python", getLicenseKey(), "us", None );

    
