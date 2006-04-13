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

import os, urllib
import inspect

__author__ = "Kun Xi < kunxi@kunxi.org >"
__version__ = "0.0.1"
__license__ = "GPL"


# Package-wide variables:
LICENSE_KEY = None;
HTTP_PROXY = None
LOCALE = "us"
VERSION = "2005-10-05"

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

# Exception class
class AWSException( Exception ) : pass
class NoLiceseKeyException( AWSException ) : pass

# Utilities functions

def _checkLocaleSupported(locale):
    if not _supportedLocales.has_key(locale):
        raise AWSException, ("Unsupported locale. Locale must be one of: %s" %
            string.join(_supportedLocales, ", "))

def setLocale(locale):
    """set locale"""
    global LOCALE
    _checkLocaleSupported(locale)
    LOCALE = locale

def getLocale():
    """get locale"""
    return LOCALE

def setLicenseKey(license_key=None):
    """set license key

    license key can come from any number of locations;
    see module docs for search order"""

    global LICENSE_KEY
    for get in _licenseKeys:
        rc = get(license_key)
        if rc: 
            LICENSE_KEY = rc;
            return;
    raise NoLiceseKeyException, ("Please get the license key from  http://www.amazon.com/webservices" )

def getLicenseKey(license_key = None):
    """get license key"""
    return LICENSE_KEY
    

def getVersion():
    """get version"""
    return VERSION

def setVersion(version):
    global VERSION
    VERSION = version
    
	
def buildURL(operation, search_index, keywords, license_key, locale, associate):
    _checkLocaleSupported(locale)
    url = "http://" + _supportedLocales[locale][1] + "/onca/xml?Service=AWSECommerceService"
    url += "&AWSAccessKeyId=%s" % license_key.strip()
    url += "&Operation=%s" % operation
    url += "&SearchIndex=%s" % search_index 
    url += "&Keywords=%s" % urllib.quote(keywords)
    return url

def buildRequest( argv ):
    url = "http://" + _supportedLocales[LOCALE][1] + "/onca/xml?Service=AWSECommerceService"
    for k,v in argv:
        if not v:
            url += '&%s=%s' % (k,v)
    return url;
    

    
def rawItemLookup( ItemId ): 
    Operation = "ItemLookup"
    AWSAccessKeyId = LICENSE_KEY
    argv = inspect.getargvalues( inspect.currentframe() )[-1].items();
    url = buildRequest( argv );
    return url;

    
    

## main functions

if __name__ == "__main__":
    setLicenseKey("1MGVS72Y8JF7EC7JDZG2")
    print rawItemLookup( "0596002815" );
    

    
